from espmega.espmega_r3 import ESPMega_standalone as ESPMega
from line_notify import LineNotify

plc = ESPMega("/espmega/ProR3", "192.168.0.26", 1883)

NOTIFY_TOKEN = "CHANGEME"
notifier = LineNotify(NOTIFY_TOKEN)

door_pin = 0

while True:
    if plc.digital_read(door_pin) == 1:
        notifier.send("Door is open")
    else:
        notifier.send("Door is closed")