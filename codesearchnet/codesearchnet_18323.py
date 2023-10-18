def create_temp_file(self, **mkstemp_kwargs) -> Tuple[int, str]:
        """
        Creates a temp file.
        :param mkstemp_kwargs: named arguments to be passed to `tempfile.mkstemp`
        :return: tuple where the first element is the file handle and the second is the location of the temp file
        """
        kwargs = {**self.default_mkstemp_kwargs, **mkstemp_kwargs}
        handle, location = tempfile.mkstemp(**kwargs)
        self._temp_files.add(location)
        return handle, location