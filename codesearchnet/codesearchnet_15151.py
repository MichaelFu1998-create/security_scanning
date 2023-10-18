def write_to_file(self, file):
        """Writes the current SVG to the :paramref:`file`.

        :param file: a file-like object
        """
        xmltodict.unparse(self._structure, file, pretty=True)