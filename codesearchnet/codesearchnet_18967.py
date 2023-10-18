def reset(self):
        """
        This command sends a reset message to the Arduino. The response tables will be reinitialized
        :return: No return value.
        """
        # set all output pins to a value of 0
        for pin in range(0, self._command_handler.total_pins_discovered):
            if self._command_handler.digital_response_table[self._command_handler.RESPONSE_TABLE_MODE] \
                    == self.PWM:
                self.analog_write(pin, 0)
            elif self._command_handler.digital_response_table[self._command_handler.RESPONSE_TABLE_MODE] \
                    == self.SERVO:
                self.analog_write(pin, 0)
            elif self._command_handler.digital_response_table[self._command_handler.RESPONSE_TABLE_MODE] \
                    == self.TONE:
                data = [self.TONE_NO_TONE, pin]
                self._command_handler.send_sysex(self._command_handler.TONE_PLAY, data)
            else:
                self.digital_write(pin, 0)
        self._command_handler.system_reset()