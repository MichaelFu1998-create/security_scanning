def get_digital_latch_data(self, pin):
        """
        This method reads the digital latch table for the specified pin and returns a list that contains:
        [latch_state, latched_data, and time_stamp].
        If the latch state is latched, the entry in the table is cleared

        :param pin:  pin number

        :return: [latch_state, latched_data, and time_stamp]
        """
        with self.pymata.data_lock:
            pin_data = self.digital_latch_table[pin]
            current_latch_data = [pin,
                                  pin_data[self.LATCH_STATE],
                                  pin_data[self.DIGITAL_LATCHED_DATA],
                                  pin_data[self.DIGITAL_TIME_STAMP],
                                  pin_data[self.DIGITAL_LATCH_CALLBACK]]
            if pin_data[self.LATCH_STATE] == self.LATCH_LATCHED:
                self.digital_latch_table[pin] = [0, 0, 0, 0, None]
        return current_latch_data