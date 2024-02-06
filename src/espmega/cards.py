from abc import ABC, abstractmethod
from espmega.connection import ESPMegaConnectionManager
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

class DigitalInputCard(Card):
    pass

class DigitalOutputCard(Card):
    pass

class AnalogCard(Card):
    pass

class ClimateCard(Card):
    pass