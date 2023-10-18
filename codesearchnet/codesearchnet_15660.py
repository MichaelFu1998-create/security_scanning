def close(self):
        """
        Closes the socket
        Called internally when Exceptions are raised
        """

        self._connected = False
        self.buf = b''

        if self.sock is not None:
            self.sock.close()