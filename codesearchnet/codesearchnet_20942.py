def rawDataReceived(self, data):
        """ Process data.

        Args:
            data (str): Incoming data
        """
        if self._len_expected is not None:
            data, extra = data[:self._len_expected], data[self._len_expected:]
            self._len_expected -= len(data)
        else:
            extra = ""

        self._buffer += data
        if self._len_expected == 0:
            data = self._buffer.strip()
            if data:
                lines = data.split("\r")
                for line in lines:
                    try:
                        message = self.factory.get_stream().get_connection().parse(line)
                        if message:
                            self.factory.get_stream().received([message])
                    except ValueError:
                        pass

            self._buffer = ""
            self._len_expected = None
            self.setLineMode(extra)