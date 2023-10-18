def _binary_file(self, file):
        """Dump the ocntent into the `file` in binary mode.
        """
        if self.__text_is_expected:
            file = TextWrapper(file, self.__encoding)
        self.__dump_to_file(file)