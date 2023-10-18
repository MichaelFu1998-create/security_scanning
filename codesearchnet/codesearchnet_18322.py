def create_temp_directory(self, **mkdtemp_kwargs) -> str:
        """
        Creates a temp directory.
        :param mkdtemp_kwargs: named arguments to be passed to `tempfile.mkdtemp`
        :return: the location of the temp directory
        """
        kwargs = {**self.default_mkdtemp_kwargs, **mkdtemp_kwargs}
        location = tempfile.mkdtemp(**kwargs)
        self._temp_directories.add(location)
        return location