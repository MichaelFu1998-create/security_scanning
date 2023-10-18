def enable_analog_reporting(self, pin):
        """
        Enables analog reporting. By turning reporting on for a single pin.

        :param pin: Analog pin number. For example for A0, the number is 0.

        :return: No return value
        """
        command = [self._command_handler.REPORT_ANALOG + pin, self.REPORTING_ENABLE]
        self._command_handler.send_command(command)