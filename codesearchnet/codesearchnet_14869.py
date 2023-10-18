def send(self, s):
        """
        Sends the given command to Niko Home Control and returns the output of
        the system.

        Aliases: write, put, sendall, send_all
        """
        self._socket.send(s.encode())
        return self.read()