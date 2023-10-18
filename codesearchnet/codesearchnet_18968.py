def set_analog_latch(self, pin, threshold_type, threshold_value, cb=None):
        """
        This method "arms" an analog pin for its data to be latched and saved in the latching table
        If a callback method is provided, when latching criteria is achieved, the callback function is called
        with latching data notification. In that case, the latching table is not updated.

        :param pin: Analog pin number (value following an 'A' designator, i.e. A5 = 5

        :param threshold_type: ANALOG_LATCH_GT | ANALOG_LATCH_LT  | ANALOG_LATCH_GTE | ANALOG_LATCH_LTE

        :param threshold_value: numerical value - between 0 and 1023

        :param cb: callback method

        :return: True if successful, False if parameter data is invalid
        """
        if self.ANALOG_LATCH_GT <= threshold_type <= self.ANALOG_LATCH_LTE:
            if 0 <= threshold_value <= 1023:
                self._command_handler.set_analog_latch(pin, threshold_type, threshold_value, cb)
                return True
        else:
            return False