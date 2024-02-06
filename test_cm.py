from espmega.connection import ESPMegaConnectionManager, ESPMegaMultiServerConnectionManager
from time import sleep

def callback1(server,topic,payload):
    print(f'callback1 {topic} {payload} on server {server}')
emc = ESPMegaMultiServerConnectionManager()
server = emc.get_server('192.168.0.26',1883)
emc.publish(server, 'test', 'hello')
emc.subscribe(server, 'test2', callback1)

print("Task completed. Waiting for callbacks...")
while True:
    emc.publish(server, 'test', 'hello keep alive')
    sleep(1)