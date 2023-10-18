def directories(self, filters=None, containing=None):
        """
        A generator that produces a sequence of paths to directories in the
        project that matches the specified filters.

        :param filters:
            the regular expressions to use when finding directories in the
            project. If not specified, all directories are returned.
        :type filters: list(str)
        :param containing:
            if a directory passes through the specified filters, it is checked
            for the presence of a file that matches one of the regular
            expressions in this parameter.
        :type containing: list(str)
        """

        filters = compile_masks(filters or [r'.*'])
        contains = compile_masks(containing)

        for dirname, files in iteritems(self._found):
            relpath = text_type(Path(dirname).relative_to(self.base_path))
            if matches_masks(relpath, filters):
                if not contains or self._contains(files, contains):
                    yield dirname