def binary_file(self, file=None):
        """Same as :meth:`file` but for binary content."""
        if file is None:
            file = BytesIO()
        self._binary_file(file)
        return file