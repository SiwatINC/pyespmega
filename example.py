from src.espmega.espmega_r3 import ESPMega_standalone as ESPMega
from time import sleep as delay

plc = ESPMega("/espmega/ProR3","192.168.0.26",1883)
plc.analog_write(7, 1, 3000)
print(plc.digital_read(1))
plc.disable_adc(0)
while(True):
    # print(plc.adc_read(0))
    # print(plc.get_input_buffer())
    print(plc.get_pwm_state_buffer())
    # print(plc.read_room_temperature())
    # plc.analog_write(7, 1, 3000)
    # print(plc.digital_read(1))
    # plc.digital_write(1, 1)
    # print(plc.get_input_buffer())
    # print(plc.get_ac_mode())
    # print(plc.get_ac_temperature())
    # delay(1)
    # plc.set_ac_mode("cool")
    # plc.set_ac_temperature(25)
    pass