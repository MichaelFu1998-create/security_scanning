def is_excluded(self, path):
        """
        Determines whether or not the specified file is excluded by the
        project's configuration.

        :param path: the path to check
        :type path: pathlib.Path
        :rtype: bool
        """

        relpath = path.relative_to(self.base_path).as_posix()
        return matches_masks(relpath, self.excludes)