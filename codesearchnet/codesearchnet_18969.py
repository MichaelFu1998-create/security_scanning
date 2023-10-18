def set_digital_latch(self, pin, threshold_type, cb=None):
        """
        This method "arms" a digital pin for its data to be latched and saved in the latching table
        If a callback method is provided, when latching criteria is achieved, the callback function is called
        with latching data notification. In that case, the latching table is not updated.

        :param pin: Digital pin number

        :param threshold_type: DIGITAL_LATCH_HIGH | DIGITAL_LATCH_LOW

        :param cb: callback function

        :return: True if successful, False if parameter data is invalid
        """
        if 0 <= threshold_type <= 1:
            self._command_handler.set_digital_latch(pin, threshold_type, cb)
            return True
        else:
            return False