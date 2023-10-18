def file(self, file=None):
        """Saves the dump in a file-like object in text mode.

        :param file: :obj:`None` or a file-like object.
        :return: a file-like object

        If :paramref:`file` is :obj:`None`, a new :class:`io.StringIO`
        is returned.
        If :paramref:`file` is not :obj:`None` it should be a file-like object.

        The content is written to the file. After writing, the file's
        read/write position points behind the dumped content.
        """
        if file is None:
            file = StringIO()
        self._file(file)
        return file