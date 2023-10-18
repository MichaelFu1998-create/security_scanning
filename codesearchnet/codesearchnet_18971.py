def set_sampling_interval(self, interval):
        """
        This method sends the desired sampling interval to Firmata.
        Note: Standard Firmata  will ignore any interval less than 10 milliseconds

        :param interval: Integer value for desired sampling interval in milliseconds

        :return: No return value.
        """
        data = [interval & 0x7f, (interval >> 7) & 0x7f]
        self._command_handler.send_sysex(self._command_handler.SAMPLING_INTERVAL, data)