def set_timeout(self, timeout):
        """Set the timeout for the communication with the device."""
        timeout = int(timeout) # will raise on Error
        self._timeout = timeout == 0 and 999999 or timeout