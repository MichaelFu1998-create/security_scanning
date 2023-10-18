def sonar_data(self, data):
        """
        This method handles the incoming sonar data message and stores
        the data in the response table.

        :param data: Message data from Firmata

        :return: No return value.
        """
        val = int((data[self.MSB] << 7) + data[self.LSB])
        pin_number = data[0]
        with self.pymata.data_lock:
            sonar_pin_entry = self.active_sonar_map[pin_number]
            # also write it into the digital response table
            self.digital_response_table[data[self.RESPONSE_TABLE_MODE]][self.RESPONSE_TABLE_PIN_DATA_VALUE] = val
            # send data through callback if there is a callback function for the pin
            if sonar_pin_entry[0] is not None:
                # check if value changed since last reading
                if sonar_pin_entry[1] != val:
                    self.active_sonar_map[pin_number][0]([self.pymata.SONAR, pin_number, val])
            # update the data in the table with latest value
            sonar_pin_entry[1] = val
            self.active_sonar_map[pin_number] = sonar_pin_entry