def get_dirs(self) -> List[str]:
        """
        Get all effect directories for registered effects.
        """
        for package in self.packages:
            yield os.path.join(package.path, 'resources')