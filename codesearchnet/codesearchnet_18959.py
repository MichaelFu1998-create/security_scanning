def i2c_config(self, read_delay_time=0, pin_type=None, clk_pin=0, data_pin=0):
        """
        NOTE: THIS METHOD MUST BE CALLED BEFORE ANY I2C REQUEST IS MADE
        This method initializes Firmata for I2c operations.
        It allows setting of a read time delay amount, and to optionally track
        the pins as I2C in the appropriate response table.
        To track pins: Set the pin_type to ANALOG or DIGITAL and provide the pin numbers.
        If using ANALOG, pin numbers use the analog number, for example A4: use 4.

        :param read_delay_time: an optional parameter, default is 0

        :param pin_type: ANALOG or DIGITAL to select response table type to track pin numbers

        :param clk_pin: pin number (see comment above).

        :param data_pin: pin number (see comment above).

        :return: No Return Value
        """
        data = [read_delay_time & 0x7f, (read_delay_time >> 7) & 0x7f]
        self._command_handler.send_sysex(self._command_handler.I2C_CONFIG, data)

        # If pin type is set, set pin mode in appropriate response table for these pins
        if pin_type:
            if pin_type == self.DIGITAL:
                self._command_handler.digital_response_table[clk_pin][self._command_handler.RESPONSE_TABLE_MODE] \
                    = self.I2C
                self._command_handler.digital_response_table[data_pin][self._command_handler.RESPONSE_TABLE_MODE] \
                    = self.I2C
            else:
                self._command_handler.analog_response_table[clk_pin][self._command_handler.RESPONSE_TABLE_MODE] \
                    = self.I2C
                self._command_handler.analog_response_table[data_pin][self._command_handler.RESPONSE_TABLE_MODE] \
                    = self.I2C