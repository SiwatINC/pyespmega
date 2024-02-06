from espmega.espmega_conn import ESPMegaMultiServerConnectionManager

emc = ESPMegaMultiServerConnectionManager()
server = emc.add_server('192.168.0.26',1883)

emc.publish(server, 'test', 'hello')