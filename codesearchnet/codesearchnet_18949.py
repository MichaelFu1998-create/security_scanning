def digital_read(self, pin):
        """
        Retrieve the last digital data value received for the specified pin.
        NOTE: This command will return values for digital, pwm, etc,  pin types

        :param pin: Selected pin

        :return: The last value entered into the digital response table.
        """
        with self.data_lock:
            data = \
                self._command_handler.digital_response_table[pin][self._command_handler.RESPONSE_TABLE_PIN_DATA_VALUE]
        return data