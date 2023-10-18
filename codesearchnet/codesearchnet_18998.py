def system_reset(self):
        """
        Send the reset command to the Arduino.
        It resets the response tables to their initial values

        :return: No return value
        """
        data = chr(self.SYSTEM_RESET)
        self.pymata.transport.write(data)

        # response table re-initialization
        # for each pin set the mode to input and the last read data value to zero
        with self.pymata.data_lock:
            # remove all old entries from existing tables
            for _ in range(len(self.digital_response_table)):
                self.digital_response_table.pop()

            for _ in range(len(self.analog_response_table)):
                self.analog_response_table.pop()

            # reinitialize tables
            for pin in range(0, self.total_pins_discovered):
                response_entry = [self.pymata.INPUT, 0, None]
                self.digital_response_table.append(response_entry)

            for pin in range(0, self.number_of_analog_pins_discovered):
                response_entry = [self.pymata.INPUT, 0, None]
                self.analog_response_table.append(response_entry)