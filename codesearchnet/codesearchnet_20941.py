def lineReceived(self, line):
        """ Callback issued by twisted when new line arrives.

        Args:
            line (str): Incoming line
        """
        while self._in_header:
            if line:
                self._headers.append(line)
            else:
                http, status, message = self._headers[0].split(" ", 2)
                status = int(status)
                if status == 200:
                    self.factory.get_stream().connected()
                else:
                    self.factory.continueTrying = 0
                    self.transport.loseConnection()
                    self.factory.get_stream().disconnected(RuntimeError(status, message))
                    return

                self._in_header = False
            break
        else:
            try:
                self._len_expected = int(line, 16)
                self.setRawMode()
            except:
                pass