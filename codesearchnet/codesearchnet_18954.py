def enable_digital_reporting(self, pin):
        """
        Enables digital reporting. By turning reporting on for all 8 bits in the "port" -
        this is part of Firmata's protocol specification.

        :param pin: Pin and all pins for this port

        :return: No return value
        """
        port = pin // 8
        command = [self._command_handler.REPORT_DIGITAL + port, self.REPORTING_ENABLE]
        self._command_handler.send_command(command)