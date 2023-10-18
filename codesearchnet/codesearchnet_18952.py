def disable_digital_reporting(self, pin):
        """
        Disables digital reporting. By turning reporting off for this pin, reporting
        is disabled for all 8 bits in the "port" -

        :param pin: Pin and all pins for this port

        :return: No return value
        """
        port = pin // 8
        command = [self._command_handler.REPORT_DIGITAL + port, self.REPORTING_DISABLE]
        self._command_handler.send_command(command)