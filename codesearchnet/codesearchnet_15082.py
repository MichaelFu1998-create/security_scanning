def _path(self, path):
        """Saves the dump in a file named `path`."""
        mode, encoding = self._mode_and_encoding_for_open()
        with open(path, mode, encoding=encoding) as file:
            self.__dump_to_file(file)