def _readline(self):
        """Read a line from the server. Data is read from the socket until a character ``\n`` is found

        :return: the read line
        :rtype: string

        """
        line = ''
        while 1:
            readable, _, __ = select.select([self.sock], [], [], 0.5)
            if self._stop:
                break
            if not readable:
                continue
            data = readable[0].recv(1)
            if data == '\n':
                break
            line += unicode(data, self.encoding)
        return line