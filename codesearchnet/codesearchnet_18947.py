def analog_write(self, pin, value):
        """
        Set the specified pin to the specified value.

        :param pin: Pin number

        :param value: Pin value

        :return: No return value
        """

        if self._command_handler.ANALOG_MESSAGE + pin < 0xf0:
            command = [self._command_handler.ANALOG_MESSAGE + pin, value & 0x7f, (value >> 7) & 0x7f]
            self._command_handler.send_command(command)
        else:
            self.extended_analog(pin, value)