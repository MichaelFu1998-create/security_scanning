def _temporary_file(self, delete):
        """:return: a temporary file where the content is dumped to."""
        file = NamedTemporaryFile("w+", delete=delete,
                                  encoding=self.__encoding)
        self._file(file)
        return file