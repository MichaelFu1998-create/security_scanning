def _bundle_exists(self, path):
        """Checks if a bundle exists at the provided path

        :param path: Bundle path
        :return: bool
        """

        for attached_bundle in self._attached_bundles:
            if path == attached_bundle.path:
                return True

        return False