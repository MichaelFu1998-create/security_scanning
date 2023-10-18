def files(self, filters=None):
        """
        A generator that produces a sequence of paths to files in the project
        that matches the specified filters.

        :param filters:
            the regular expressions to use when finding files in the project.
            If not specified, all files are returned.
        :type filters: list(str)
        """

        filters = compile_masks(filters or [r'.*'])

        for files in itervalues(self._found):
            for file_ in files:
                relpath = text_type(Path(file_).relative_to(self.base_path))
                if matches_masks(relpath, filters):
                    yield file_