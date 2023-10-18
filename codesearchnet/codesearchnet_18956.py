def extended_analog(self, pin, data):
        """
        This method will send an extended data analog output command to the selected pin

        :param pin: 0 - 127

        :param data: 0 - 0xfffff
        """
        analog_data = [pin, data & 0x7f, (data >> 7) & 0x7f, (data >> 14) & 0x7f]
        self._command_handler.send_sysex(self._command_handler.EXTENDED_ANALOG, analog_data)