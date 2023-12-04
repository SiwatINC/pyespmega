from espmega.espmega_r3 import ESPMega_standalone as ESPMega
from scipy import signal

plc = ESPMega("/espmega/ProR3", "192.168.0.26", 1883)

set_point = 60

poles = [-3, -4, 0, 0]
zeros = [-1, -2]
gain = 150

transfer_function = signal.TransferFunction(zeros, poles, gain)

while True:
    current_temperature = plc.read_room_temperature()

    # control the heater
    value = transfer_function.output(current_temperature)
    plc.analog_write(0, True, value)
