def handle_read(self):
        """
        Accept any incoming connections.
        """
        with self._lock:
            logger.debug("handle_read()")
            if self._socket is None:
                return
            while True:
                try:
                    sock, address = self._socket.accept()
                except socket.error, err:
                    if err.args[0] in BLOCKING_ERRORS:
                        break
                    else:
                        raise
                logger.debug("Accepted connection from: {0!r}".format(address))
                self._target(sock, address)