def receive(self):
        """Receive TCP response, looping to get whole thing or timeout."""
        try:
            buffer = self._socket.recv(BUFFER_SIZE)
        except socket.timeout as error:
            # Something is wrong, assume it's offline temporarily
            _LOGGER.error("Error receiving: %s", error)
            # self._socket.close()
            return ""

        # Read until a newline or timeout
        buffering = True
        response = ''
        while buffering:
            if '\n' in buffer.decode("utf8"):
                response = buffer.decode("utf8").split('\n')[0]
                buffering = False
            else:
                try:
                    more = self._socket.recv(BUFFER_SIZE)
                except socket.timeout:
                    more = None
                if not more:
                    buffering = False
                    response = buffer.decode("utf8")
                else:
                    buffer += more
        return response