def _extract_packages(self):
        """
        Extract a package in a new temporary directory.
        """
        self.path_unpacked = mkdtemp(prefix="scoap3_package_",
                                     dir=CFG_TMPSHAREDDIR)
        for path in self.retrieved_packages_unpacked:
            scoap3utils_extract_package(path, self.path_unpacked, self.logger)

        return self.path_unpacked