def _binary_temporary_file(self, delete):
        """:return: a binary temporary file where the content is dumped to."""
        file = NamedTemporaryFile("wb+", delete=delete)
        self._binary_file(file)
        return file