def disable_analog_reporting(self, pin):
        """
        Disables analog reporting for a single analog pin.

        :param pin: Analog pin number. For example for A0, the number is 0.

        :return: No return value
        """
        command = [self._command_handler.REPORT_ANALOG + pin, self.REPORTING_DISABLE]
        self._command_handler.send_command(command)