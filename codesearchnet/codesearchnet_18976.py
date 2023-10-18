def stepper_request_library_version(self):
        """
        Request the stepper library version from the Arduino.
        To retrieve the version after this command is called, call
        get_stepper_version
        """
        data = [self.STEPPER_LIBRARY_VERSION]
        self._command_handler.send_sysex(self._command_handler.STEPPER_DATA, data)