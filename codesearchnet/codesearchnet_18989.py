def get_analog_latch_data(self, pin):
        """
        This method reads the analog latch table for the specified pin and returns a list that contains:
        [latch_state, latched_data, and time_stamp].
        If the latch state is latched, the entry in the table is cleared

        :param pin:  pin number

        :return: [latch_state, latched_data, and time_stamp]
        """
        with self.pymata.data_lock:
            pin_data = self.analog_latch_table[pin]
            current_latch_data = [pin,
                                  pin_data[self.LATCH_STATE],
                                  pin_data[self.ANALOG_LATCHED_DATA],
                                  pin_data[self.ANALOG_TIME_STAMP],
                                  pin_data[self.ANALOG_LATCH_CALLBACK]]
            # if this is latched data, clear the latch table entry for this pin
            if pin_data[self.LATCH_STATE] == self.LATCH_LATCHED:
                self.analog_latch_table[pin] = [0, 0, 0, 0, 0, None]
        return current_latch_data