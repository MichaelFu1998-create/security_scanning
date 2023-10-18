def string(self):
        """:return: the dump as a string"""
        if self.__text_is_expected:
            return self._string()
        else:
            return self._bytes().decode(self.__encoding)