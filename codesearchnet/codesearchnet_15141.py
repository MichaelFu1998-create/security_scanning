def write(self, bytes_):
        """Write bytes to the file."""
        string = bytes_.decode(self._encoding)
        self._file.write(string)