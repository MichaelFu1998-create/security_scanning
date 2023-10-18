def bytes(self):
        """:return: the dump as bytes."""
        if self.__text_is_expected:
            return self.string().encode(self.__encoding)
        else:
            return self._bytes()