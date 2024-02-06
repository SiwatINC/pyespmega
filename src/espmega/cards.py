import abc

class Card(metaclass=abc.ABCMeta):
    pass

class DigitalInputCard(Card):
    pass

class DigitalOutputCard(Card):
    pass

class AnalogCard(Card):
    pass

class ClimateCard(Card):
    pass