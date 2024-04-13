from abc import ABC, abstractmethod
from espmega.connection import ESPMegaConnectionManager, CardMQTTAdapter
class Card(ABC):
    card_id: int
    base_topic: str
    conn: ESPMegaConnectionManager
    server: str
    @abstractmethod
    def __init__(self, card_id: int, base_topic: str, conn: ESPMegaConnectionManager, server: str):
        pass
    @abstractmethod
    def subscribe_card(self):
        pass
    @abstractmethod
    def request_update(self):
        pass

class DigitalInputCard(Card):
    pass

class DigitalOutputCard(Card):
    pwm_states: list
    pwm_values: list
    mqtt: CardMQTTAdapter
    def __init__(self):
        self.pwm_states = {}
        self.pwm_values = {}
    def begin(self, card_id: int, base_topic: str, mqtt: CardMQTTAdapter):
        self.card_id = card_id
        self.base_topic = base_topic
        self.mqtt = mqtt
    def subscribe_card(self):
        # Subscribe to {base_topic}/{card_id}/{pwm_id}/state
        # and also to {base_topic}/{card_id}/{pwm_id}/value
        # There are 16 PWM pins on the ESPMega, 0-15, note that pwm_id are padded to 2 digits
        for pwm_id in range(16):
            self.mqtt.subscribe_relative(f'{pwm_id:02}/state', self._pwm_state_callback)
            self.mqtt.subscribe_relative(f'{pwm_id:02}/value', self._pwm_value_callback)
    def request_update(self):
        # Request the current state of the PWM pins
        # Pubish 'request' to {base_topic}/{card_id}/requeststate
        self.mqtt.publish_relative(f'requeststate', 'request')
    def set_pwm_state(self, pwm_id: int, state: str):
        # Publish 'state' to {base_topic}/{card_id}/{pwm_id}/state/set
        self.mqtt.publish_relative(f'{pwm_id:02}/state/set', state)
    def set_pwm_value(self, pwm_id: int, value: int):
        # Value must be an integer between 0 and 4095
        # Throw an exception if value is not in the range
        if value < 0 or value > 4095:
            raise ValueError('Value must be between 0 and 4095')
        # Publish 'value' to {base_topic}/{card_id}/{pwm_id}/value/set
        self.mqtt.publish_relative(f'{pwm_id:02}/value/set', value)
    def get_pwm_state(self, pwm_id: int) -> int:
        return self.pwm_states[pwm_id]
    def get_pwm_value(self, pwm_id: int) -> int:
        return self.pwm_values[pwm_id]
    def _mqtt_callback(self, topic: str, payload: str):
        # Parse the PWM id from the topic
        # Update the pwm_states dictionary
        # Remove the base_topic and card_id from the topic
        # Note that the base topic may contain slashes
        topic = topic.removeprefix(f'{self.mqtt.base_topic}/{self.mqtt.card_id}/')
        # Now the topic is {pwm_id}/state or {pwm_id}/value
        # First check if it actually is
        if not topic.endswith('/state') and not topic.endswith('/value') and not len(topic)!=8:
            return
        command, pwm_id = topic.split('/')
        pwm_id = int(pwm_id)
        if command == 'state':
            self.pwm_states[pwm_id] = int(payload)
        elif command == 'value':
            self.pwm_values[pwm_id] = int(payload)

class AnalogCard(Card):
    pass

class ClimateCard(Card):
    pass