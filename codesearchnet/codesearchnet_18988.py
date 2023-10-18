def set_digital_latch(self, pin, threshold_type, cb):
        """
        This method "arms" a pin to allow data latching for the pin.

        :param pin: digital pin number

        :param threshold_type: DIGITAL_LATCH_HIGH | DIGITAL_LATCH_LOW

        :param cb: User provided callback function
        """
        with self.pymata.data_lock:
            self.digital_latch_table[pin] = [self.LATCH_ARMED, threshold_type, 0, 0, cb]