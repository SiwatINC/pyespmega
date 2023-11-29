# pyESPMega
This library provides a mean of communicating with the ESPMega Programmable Logic Controller through MQTT<br/>

## **Compatibility**
This library is compatible with:<br/>
- ESPMega R2.4 [2018] (Model e)
- ESPMega R3.0 [2020] (All Model)
- ESPMega R4.0 [2023] (All Model)
- ESPMega PRO 2.0 [2018] (Model c)
- ESPMega PRO 3.3 [2023] (Model b,c)

## **ESPMega Client Types**
There are two type of ESPMega client, ESPMega and ESPMega_standalone<br/>
### ESPMega
ESPMega class requires you to provide and maintain an MQTT connection
This class takes in a Paho-MQTT Client as an input argument<br/>
**Import and Initialization**
```
from espmegar3 import ESPMega
plc = ESPMega("/basetopic", MQTT_CLIENT)
```
### ESPMega_standalone
ESPMega_standalone create and maintain the required mqtt connection for you.
**Import and Initialization**
```
from espmegar3 import ESPMega_standalone as ESPMega
plc = ESPMega("/basetopic", "MQTT_SERVER", MQTT_PORT)
```
## **ESPMega Client Functions**
1. **digital_read(pin: int)** | Reads the digital value of a pin.
2. **digital_write(pin: int, state: bool) | Writes a digital value to a pin.
3. **analog_write(pin: int, state: bool, value: int)** | Writes an analog value to a pin.
4. **dac_write(pin: int, state: bool, value: int)** | Writes a DAC value to a pin.
5. **set_ac_mode(mode: str)** | Sets the AC mode. ("off", "fan_only", "cool")
6. **set_ac_temperature(temperature: int)** | Sets the AC temperature.
        
            
        :
            
        set_ac_fan_speed(self, fan_speed: str):
            Sets the AC fan speed.
        get_ac_mode(self):
            Returns the current AC mode.
        get_ac_temperature(self):
            Returns the current AC temperature.
        get_ac_fan_speed(self):
            Returns the current AC fan speed.
        read_room_temperature(self):
            Reads the room temperature.
        read_humidity(self):
            Reads the humidity.
        send_infrared(self, code: dict):
            Sends an infrared code.
        request_state_update(self):
            Requests an update of the device state.
        get_input_buffer(self):
            Returns the input buffer.
