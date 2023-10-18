def sendall(self, line):
        """
        Send a line, or multiple lines sperapted by '\\r\\n'
        """
        if isinstance(line, APRSPacket):
            line = str(line)
        elif not isinstance(line, string_type):
            raise TypeError("Expected line to be str or APRSPacket, got %s", type(line))
        if not self._connected:
            raise ConnectionError("not connected")

        if line == "":
            return

        line = line.rstrip("\r\n") + "\r\n"

        try:
            self.sock.setblocking(1)
            self.sock.settimeout(5)
            self._sendall(line)
        except socket.error as exp:
            self.close()
            raise ConnectionError(str(exp))