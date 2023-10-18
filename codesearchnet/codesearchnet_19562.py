def send_command(self, command):
        """Send TCP command to hub and return response."""
        # use lock to make TCP send/receive thread safe
        with self._lock:
            try:
                self._socket.send(command.encode("utf8"))
                result = self.receive()
                # hub may send "status"/"new" messages that should be ignored
                while result.startswith("S") or result.startswith("NEW"):
                    _LOGGER.debug("!Got response: %s", result)
                    result = self.receive()
                _LOGGER.debug("Received: %s", result)
                return result
            except socket.error as error:
                _LOGGER.error("Error sending command: %s", error)
                # try re-connecting socket
                self.connect()
                return ""