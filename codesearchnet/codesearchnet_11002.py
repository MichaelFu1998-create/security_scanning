def find(self, path: Path):
        """
        Find a file in the path. The file may exist in multiple
        paths. The last found file will be returned.

        :param path: The path to find
        :return: The absolute path to the file or None if not found
        """
        # Update paths from settings to make them editable runtime
        # This is only possible for FileSystemFinders
        if getattr(self, 'settings_attr', None):
            self.paths = getattr(settings, self.settings_attr)

        path_found = None

        for entry in self.paths:
            abspath = entry / path
            if abspath.exists():
                path_found = abspath

        return path_found