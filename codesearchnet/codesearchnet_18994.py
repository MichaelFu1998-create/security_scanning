def encoder_data(self, data):
        """
        This method handles the incoming encoder data message and stores
        the data in the digital response table.

        :param data: Message data from Firmata

        :return: No return value.
        """
        prev_val = self.digital_response_table[data[self.RESPONSE_TABLE_MODE]][self.RESPONSE_TABLE_PIN_DATA_VALUE]
        val = int((data[self.MSB] << 7) + data[self.LSB])
        # set value so that it shows positive and negative values
        if val > 8192:
            val -= 16384
        pin = data[0]
        with self.pymata.data_lock:
            self.digital_response_table[data[self.RESPONSE_TABLE_MODE]][self.RESPONSE_TABLE_PIN_DATA_VALUE] = val
            if prev_val != val:
                callback = self.digital_response_table[pin][self.RESPONSE_TABLE_CALLBACK]
                if callback is not None:
                    callback([self.pymata.ENCODER, pin,
                              self.digital_response_table[pin][self.RESPONSE_TABLE_PIN_DATA_VALUE]])