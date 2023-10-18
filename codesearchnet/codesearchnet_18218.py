def dataReceived(self, data):
        """
        Translates bytes into lines, and calls lineReceived.

        Copied from ``twisted.protocols.basic.LineOnlyReceiver`` but using
        str.splitlines() to split on ``\r\n``, ``\n``, and ``\r``.
        """
        self.resetTimeout()
        lines = (self._buffer + data).splitlines()

        # str.splitlines() doesn't split the string after a trailing newline
        # character so we must check if there is a trailing newline and, if so,
        # clear the buffer as the line is "complete". Else, the line is
        # incomplete and we keep the last line in the buffer.
        if data.endswith(b'\n') or data.endswith(b'\r'):
            self._buffer = b''
        else:
            self._buffer = lines.pop(-1)

        for line in lines:
            if self.transport.disconnecting:
                # this is necessary because the transport may be told to lose
                # the connection by a line within a larger packet, and it is
                # important to disregard all the lines in that packet following
                # the one that told it to close.
                return
            if len(line) > self._max_length:
                self.lineLengthExceeded(line)
                return
            else:
                self.lineReceived(line)
        if len(self._buffer) > self._max_length:
            self.lineLengthExceeded(self._buffer)
            return