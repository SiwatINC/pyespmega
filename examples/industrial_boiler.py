from espmega.espmega_r3 import ESPMega_standalone as ESPMega
from time import sleep as delay
from time import perf_counter as clock
from simple_pid import PID
from math import log

# Thermistor parameters
R1 = 50000  # Bias resistor value in ohms
R2 = 100000  # Thermistor resistance at reference temperature in ohms
T0 = 298.15  # Reference temperature in Kelvin
B = 3950  # Beta coefficient of the thermistor

def adc_to_temp(adc_value):
    # Convert ADC value to voltage
    voltage = adc_value * (12 / 65535)

    # Convert voltage to resistance using voltage divider formula
    resistance = (R1 * voltage) / (12 - voltage)

    # Convert resistance to temperature using Steinhart-Hart equation
    steinhart = (resistance / R2) - 1
    steinhart = B / steinhart
    steinhart += 1 / T0
    steinhart = 1 / steinhart
    temperature = steinhart - 273.15  # Convert temperature to Celsius

    return temperature

plc = ESPMega("/espmega/ProR3", "192.168.0.26", 1883)
pid = PID(1, 0.1, 0.05, setpoint=100, sample_time=0.1, output_limits=(0, 4095))

# Digital PWM Outputs
inlet_valve_pin = 0
outlet_valve_pin = 1

# True Analog Outputs
boiler_heater_pin = 0

# Analog Inputs
boiler_temperature_sensor_pin = 0

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
    # Start measuring the time
    start_time = clock()
    # Wait until the temperature reaches the threshold or the time is up
    while plc.analog_read(temp_sensor_pin) < temp_threshold:
        if clock() - start_time > boil_time:
            break
        current_temperature = adc_to_temp(plc.analog_read(boiler_temperature_sensor_pin))
        actuator_value = pid(current_temperature)
        plc.analog_write(boiler_heater_pin, actuator_value)
        delay(0.1)
    # Turn off the boiler heater
    plc.dac_write(boiler_heater_pin, 0)
    # Open the outlet valve
    plc.digital_write(outlet_valve_pin, 1)
    # Start draining the boiler
    delay(drain_time)
    # Close the outlet valve
    plc.digital_write(outlet_valve_pin, 0)

while True:
    boiler_plant()
    

