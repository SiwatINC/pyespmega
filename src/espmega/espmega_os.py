from espmega.connection import ESPMegaMultiServerConnectionManager
from time import sleep
from cards import Card, DigitalInputCard, DigitalOutputCard


class ESPMegaOS:
    mcm = ESPMegaMultiServerConnectionManager
    server: str
    mqtt_server: str
    mqtt_port: int
    mqtt_use_auth: bool
    mqtt_username: str
    mqtt_password: str
    cards: dict = {}
    def __init__(self, mqtt_server: str, mqtt_port: int, mqtt_use_auth: bool = False,mqtt_username: str = None, mqtt_password: str = None):
        self.mcm = ESPMegaMultiServerConnectionManager()
        self.mqtt_server = mqtt_server
        self.mqtt_port = mqtt_port
        self.mqtt_use_auth = mqtt_use_auth
        self.mqtt_username = None
        self.mqtt_password = None
        if not self.mqtt_use_auth:
            self.mcm.get_server(self.mqtt_server, self.mqtt_port)
        else:
            self.mcm.get_server(self.mqtt_server, self.mqtt_port, self.mqtt_use_auth, self.mqtt_username, self.mqtt_password)
    def _subscribe(self, topic: str, callback: callable):
        self.mcm.subscribe(self.server, topic, callback)
    def _publish(self, topic: str, payload: str):
        self.mcm.publish(self.server, topic, payload)
    def register_card(self, card: Card):
        self.cards[card.card_id] = card
    def subscribe_cards(self):
        for card in self.cards:
            self.cards[card].subscribe_card()
    def request_updates(self):
        for card in self.cards:
            self.cards[card].request_update()