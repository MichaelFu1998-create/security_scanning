def modules(self, filters=None):
        """
        A generator that produces a sequence of paths to files that look to be
        Python modules (e.g., ``*.py``).

        :param filters:
            the regular expressions to use when finding files in the project.
            If not specified, all files are returned.
        :type filters: list(str)
        """

        masks = compile_masks(r'\.py$')
        for file_ in self.files(filters=filters):
            if matches_masks(file_, masks):
                yield file_