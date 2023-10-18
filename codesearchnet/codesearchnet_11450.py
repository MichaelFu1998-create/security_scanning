def sys_paths(self, filters=None):
        """
        Produces a list of paths that would be suitable to use in ``sys.path``
        in order to access the Python modules/packages found in this project.

        :param filters:
            the regular expressions to use when finding files in the project.
            If not specified, all files are returned.
        :type filters: list(str)
        """

        paths = set()

        packages = list(self.packages(filters=filters))

        for module in self.modules(filters=filters):
            parent = text_type(Path(module).parent)
            if parent not in packages:
                paths.add(parent)

        paths.update(self.topmost_directories([
            text_type(Path(package).parent)
            for package in packages
        ]))

        return list(paths)