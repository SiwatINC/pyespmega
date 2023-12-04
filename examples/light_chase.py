from espmega.espmega_r3 import ESPMega_standalone as ESPMega
import time

plc = ESPMega("/espmega/ProR3","192.168.0.26",1883)

num_leds: int = 4

# Set the initial state of the LEDs
for i in range(num_leds):
    plc.digital_write(i, 0)

# Light chasing effect
while True:
    for i in range(num_leds):
        plc.digital_write(i, 1)  # Turn on the current LED
        time.sleep(0.5)  # Delay for a certain period
        plc.digital_write(i, 0)  # Turn off the current LED

