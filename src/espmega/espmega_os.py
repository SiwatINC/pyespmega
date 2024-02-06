from espmega.connection import ESPMegaMultiServerConnectionManager
from time import sleep


class ESPMegaOS:
    mcm = ESPMegaMultiServerConnectionManager
    server: str
    mqtt_server: str
    mqtt_port: int
    mqtt_use_auth: bool
    mqtt_username: str
    mqtt_password: str
    def __init__(self, mqtt_server: str, mqtt_port: int, mqtt_use_auth: bool = False,):
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