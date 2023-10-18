def is_excluded_dir(self, path):
        """
        Determines whether or not the specified directory is excluded by the
        project's configuration.

        :param path: the path to check
        :type path: pathlib.Path
        :rtype: bool
        """

        if self.is_excluded(path):
            return True
        return matches_masks(path.name, ALWAYS_EXCLUDED_DIRS)