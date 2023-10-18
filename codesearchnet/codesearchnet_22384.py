def add_directory(self, *args, **kwargs):
        """
        Add directory or directories list to bundle

        :param exclusions: List of excluded paths

        :type path: str|unicode
        :type exclusions: list
        """
        exc = kwargs.get('exclusions', None)
        for path in args:
            self.files.append(DirectoryPath(path, self, exclusions=exc))