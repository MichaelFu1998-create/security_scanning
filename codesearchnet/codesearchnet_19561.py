def connect(self):
        """Create and connect to socket for TCP communication with hub."""
        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._socket.settimeout(TIMEOUT_SECONDS)
            self._socket.connect((self._ip, self._port))
            _LOGGER.debug("Successfully created Hub at %s:%s :)", self._ip,
                          self._port)
        except socket.error as error:
            _LOGGER.error("Error creating Hub: %s :(", error)
            self._socket.close()