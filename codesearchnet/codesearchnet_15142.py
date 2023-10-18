def write(self, string):
        """Write a string to the file."""
        bytes_ = string.encode(self._encoding)
        self._file.write(bytes_)