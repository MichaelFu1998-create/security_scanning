def set_analog_latch(self, pin, threshold_type, threshold_value, cb):
        """
        This method "arms" a pin to allow data latching for the pin.

        :param pin: Analog pin number (value following an 'A' designator, i.e. A5 = 5

        :param threshold_type: ANALOG_LATCH_GT | ANALOG_LATCH_LT  | ANALOG_LATCH_GTE | ANALOG_LATCH_LTE

        :param threshold_value: numerical value

        :param cb: User provided callback function
        """
        with self.pymata.data_lock:
            self.analog_latch_table[pin] = [self.LATCH_ARMED, threshold_type, threshold_value, 0, 0, cb]