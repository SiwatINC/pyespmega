from espmega.espmega_r3 import ESPMega_standalone as ESPMega
from time import sleep as delay

plc = ESPMega("/facescan","192.168.0.239",1883)
plc.analog_write(7, 1, 3000)
print(plc.digital_read(1))