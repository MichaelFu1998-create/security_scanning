def _file(self, file):
        """Dump the content to a `file`.
        """
        if not self.__text_is_expected:
            file = BytesWrapper(file, self.__encoding)
        self.__dump_to_file(file)