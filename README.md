# pyESPMega
This library provides a mean of communicating with the ESPMega Programmable Logic Controller through MQTT

There are two type of ESPMega class, ESPMega and ESPMega_standalone<br/>
The only difference is that ESPMega requires you to provide and maintain an MQTT connection
while ESPMega_standalone create and maintain the required mqtt connection for you.

Methods:
        __init__(self, base_topic: str, mqtt: pahomqtt.Client, mqtt_callback = None, input_callback = None):
            Initializes the ESPMega object.
        digital_read(self, pin: int) -> bool:
            Reads the digital value of a pin.
        digital_write(self, pin: int, state: bool) -> None:
            Writes a digital value to a pin.
        analog_write(self, pin: int, state: bool, value: int):
            Writes an analog value to a pin.
        dac_write(self, pin: int, state: bool, value: int):
            Writes a DAC value to a pin.
        set_ac_mode(self, mode: str):
            Sets the AC mode.
        set_ac_temperature(self, temperature: int):
            Sets the AC temperature.
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
        handle_message(self, client: pahomqtt.Client, data, message: pahomqtt.MQTTMessage):
            Handles incoming MQTT messages.
        get_input_buffer(self):
            Returns the input buffer.
