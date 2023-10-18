def _parse(self, filename):
        """Opens data file and for each line, calls _eat_name_line"""
        self.names = {}
        with codecs.open(filename, encoding="iso8859-1") as f:
            for line in f:
                if any(map(lambda c: 128 < ord(c) < 160, line)):
                    line = line.encode("iso8859-1").decode("windows-1252")
                self._eat_name_line(line.strip())