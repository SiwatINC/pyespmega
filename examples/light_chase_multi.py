from espmega.espmega_r3 import ESPMega
from paho.mqtt import client
import time

mqtt = client.Client("python_emgclient")
mqtt.connect("192.168.0.26", 1883)
mqtt.loop_start()

plcs = []
num_plcs = 7
num_leds = 4

# Initialize the PLC objects
for i in range(num_plcs):
    plc_topic = f"/plc/m2{i+1}"
    plcs.append(ESPMega(plc_topic, mqtt=mqtt))

# Set the initial state of the LEDs
for plc in plcs:
    for i in range(num_leds):
        plc.digital_write(i, 0)

# Light chasing effect
while True:
    for plc_index, plc in enumerate(plcs):
        for i in range(num_leds):
            plc.digital_write(i, 1)  # Turn on the current LED
            time.sleep(0.5)  # Delay for a certain period
            plc.digital_write(i, 0)  # Turn off the current LED
        if plc_index < num_plcs - 1:
            plcs[plc_index + 1].digital_write(0, 1)  # Turn on the first LED of the next PLC
        time.sleep(0.5)  # Delay before moving to the next PLC
