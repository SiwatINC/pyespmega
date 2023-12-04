from espmega.espmega_r3 import ESPMega_standalone as ESPMega
from time import sleep as delay
from time import perf_counter as clock
plc = ESPMega("/espmega/ProR3", "192.168.0.26", 1883)

inlet_valve_pin = 0
outlet_valve_pin = 1
boiler_heater_pin = 2

temp_sensor_pin = 0
temp_threshold = 120

boil_time = 100
fill_time = 5
drain_time = 10

# Boiler plant implementation
def boiler_plant():
    # Open the inlet valve
    plc.digital_write(inlet_valve_pin, 1)
    # Start filling the boiler
    delay(fill_time)
    # Close the inlet valve
    plc.digital_write(inlet_valve_pin, 0)
    # Turn on the boiler heater
    plc.digital_write(boiler_heater_pin, 1)
    # Start measuring the time
    start_time = clock()
    # Wait until the temperature reaches the threshold or the time is up
    while plc.analog_read(temp_sensor_pin) < temp_threshold:
        if clock() - start_time > boil_time:
            break
        delay(1)
    # Turn off the boiler heater
    plc.digital_write(boiler_heater_pin, 0)
    # Open the outlet valve
    plc.digital_write(outlet_valve_pin, 1)
    # Start draining the boiler
    delay(drain_time)
    # Close the outlet valve
    plc.digital_write(outlet_valve_pin, 0)

while True:
    boiler_plant()
    

