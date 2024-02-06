import paho.mqtt.client as pahomqtt
from time import sleep


class ESPMegaOS:
    mqtt: pahomqtt.Client