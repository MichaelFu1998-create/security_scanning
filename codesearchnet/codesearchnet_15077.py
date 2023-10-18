def _bytes(self):
        """:return: bytes from a :class:`io.BytesIO`"""
        file = BytesIO()
        self.__dump_to_file(file)
        file.seek(0)
        return file.read()