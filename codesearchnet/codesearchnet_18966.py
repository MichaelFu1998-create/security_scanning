def refresh_report_version(self):
        """
        This method will query firmata for the report version.
        Retrieve the report version via a call to get_firmata_version()
        """
        command = [self._command_handler.REPORT_VERSION]
        self._command_handler.send_command(command)