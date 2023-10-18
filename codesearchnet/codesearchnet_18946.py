def analog_read(self, pin):
        """
        Retrieve the last analog data value received for the specified pin.

        :param pin: Selected pin

        :return: The last value entered into the analog response table.
        """
        with self.data_lock:
            data = self._command_handler.analog_response_table[pin][self._command_handler.RESPONSE_TABLE_PIN_DATA_VALUE]
        return data