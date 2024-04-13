import paho.mqtt.client as pahomqtt
import threading
import re
import time
from functools import partial
class ESPMegaMQTTSubscription:
    topic: str
    callback: callable
    def __init__(self, topic: str, callback: callable):
        self.topic = topic
        self.callback = callback

class ESPMegaConnectionManager:
    callbacks_map = {}
    callback_id_counter: int = 0
    mqtt: pahomqtt.Client
    mqtt_server: str
    mqtt_port: int
    mqtt_use_auth: bool
    mqtt_username: str
    mqtt_password: str
    mqtt_thread: threading.Thread
    def __init__(self,mqtt_server: str, mqtt_port: int, mqtt_use_auth: bool = False,
                 mqtt_username: str = None, mqtt_password: str = None):
        self.mqtt = pahomqtt.Client()
        self.mqtt_server = mqtt_server
        self.mqtt_port = mqtt_port
        self.mqtt_use_auth = mqtt_use_auth
        self.mqtt_username = mqtt_username
        self.mqtt_password = mqtt_password
        self.mqtt.on_message = self._callback
        self.mqtt_thread = threading.Thread(target=self._keep_alive)
        self.mqtt_thread.start()
        self.mqtt.loop_start()
    def subscribe(self, topic: str, callback: callable) -> int:
        self.callbacks_map[self.callback_id_counter] = ESPMegaMQTTSubscription(topic, callback)
        self.callback_id_counter += 1
        self._subscribe()
    def unsubscribe(self, callback_id: int):
        topic = self.callbacks_map[callback_id].topic
        self.callbacks_map.pop(callback_id)
        # Is any other callback subscribed to the same topic?
        # If not, unsubscribe from the topic
        if not any(sub.callback for sub in self.callbacks_map.values() if sub.topic == topic):
            self.mqtt.unsubscribe(topic)
    def connect(self):
        if self.mqtt_use_auth:
            self.mqtt.username_pw_set(self.mqtt_username, self.mqtt_password)
        else:
            self.mqtt.connect(self.mqtt_server, self.mqtt_port, 60)
        if self.mqtt.is_connected():
            self._subscribe()
    def publish(self, topic: str, payload: str):
        self.mqtt.publish(topic, payload)
    def _callback(self, client, userdata, message):
        message: str  = message.encode('utf-8')
        for sub in self.callbacks_map.values():
            pattern = sub.topic.replace('+', '[^/]+').replace('#', '.+')
            if re.match(pattern, message.topic):
                sub.callback(message.topic,message.payload)
    def _subscribe(self):
        for sub in self.callbacks_map.values():
            self.mqtt.subscribe(sub.topic)
    def _keep_alive(self):
        while True:
            if not self.mqtt.is_connected():
                self.connect()
                self._subscribe()
            time.sleep(5)

class ESPMegaMultiServerConnectionManager:
    connection_managers = {}
    def __init__(self):
        pass
    def get_server_name(self, mqtt_server: str, mqtt_port: int) -> str:
        return f'{mqtt_server}:{mqtt_port}'
    def get_server(self, mqtt_server: str, mqtt_port: int, mqtt_use_auth: bool = False,
                   mqtt_username: str = None, mqtt_password: str = None, mqtt_client_id: str = None) -> str:
        server_name = self.get_server_name(mqtt_server, mqtt_port)
        if server_name not in self.connection_managers:
            self.connection_managers[server_name] = ESPMegaConnectionManager(mqtt_server, mqtt_port, mqtt_use_auth,
                                                                        mqtt_username, mqtt_password)
            time.sleep(3)
        return server_name
    def publish(self, server_name: str, topic: str, payload: str):
        self.connection_managers[server_name].publish(topic, payload)
    def subscribe(self, server_name: str, topic: str, callback: callable) -> int:
        callback_wrapper = partial(callback, server_name)
        return self.connection_managers[server_name].subscribe(topic, callback_wrapper)
    def unsubscribe(self, server_name: str, callback_id: int):
        self.connection_managers[server_name].unsubscribe(callback_id)

# This class provides a way for a card object representation to interact with the MQTT broker
# The adapater object is created by the ESPMegaOS object and passed to the card object
class CardMQTTAdapter:
    card_id: int
    base_topic: str
    conn: ESPMegaConnectionManager
    server: str
    def __init__(self, card_id: int, base_topic: str, conn: ESPMegaConnectionManager):
        self.card_id = card_id
        self.base_topic = base_topic
        self.conn = conn
    def subscribe_relative(self, topic: str, callback: callable):
        self.conn.subscribe(f'{self.base_topic}/{self.card_id}/{topic}', callback)
    def publish_relative(self, topic: str, payload: str):
        self.conn.publish(f'{self.base_topic}/{self.card_id}/{topic}', payload)
    def subscribe_absolute(self, topic: str, callback: callable):
        self.conn.subscribe(topic, callback)
    def publish_absolute(self, topic: str, payload: str):
        self.conn.publish(topic, payload)