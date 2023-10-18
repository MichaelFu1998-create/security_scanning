def set_pin_mode(self, pin, mode, pin_type, cb=None):
        """
        This method sets a pin to the desired pin mode for the pin_type.
        It automatically enables data reporting.
        NOTE: DO NOT CALL THIS METHOD FOR I2C. See i2c_config().

        :param pin: Pin number (for analog use the analog number, for example A4: use 4)

        :param mode: INPUT, OUTPUT, PWM, PULLUP

        :param pin_type: ANALOG or DIGITAL

        :param cb: This is an optional callback function to report data changes to the user

        :return: No return value
        """
        command = [self._command_handler.SET_PIN_MODE, pin, mode]
        self._command_handler.send_command(command)

        # enable reporting for input pins
        if mode == self.INPUT or mode == self.PULLUP:
            if pin_type == self.ANALOG:

                # set analog response table to show this pin is an input pin

                self._command_handler.analog_response_table[pin][self._command_handler.RESPONSE_TABLE_MODE] = \
                    self.INPUT
                self._command_handler.analog_response_table[pin][self._command_handler.RESPONSE_TABLE_CALLBACK] = cb
                self.enable_analog_reporting(pin)
            # if not analog it has to be digital
            else:
                self._command_handler.digital_response_table[pin][self._command_handler.RESPONSE_TABLE_MODE] = \
                    self.INPUT
                self._command_handler.digital_response_table[pin][self._command_handler.RESPONSE_TABLE_CALLBACK] = cb

                self.enable_digital_reporting(pin)

        else:  # must be output - so set the tables accordingly
            if pin_type == self.ANALOG:
                self._command_handler.analog_response_table[pin][self._command_handler.RESPONSE_TABLE_MODE] = mode

            else:
                self._command_handler.digital_response_table[pin][self._command_handler.RESPONSE_TABLE_MODE] = mode