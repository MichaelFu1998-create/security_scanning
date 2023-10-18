def _extract_packages(self):
        """
        Extract a package in a new directory.
        """
        if not hasattr(self, "retrieved_packages_unpacked"):
            self.retrieved_packages_unpacked = [self.package_name]
        for path in self.retrieved_packages_unpacked:
            package_name = basename(path)
            self.path_unpacked = join(CFG_UNPACKED_FILES,
                                      package_name.split('.')[0])
            self.logger.debug("Extracting package: %s"
                              % (path.split("/")[-1],))
            try:
                if "_archival_pdf" in self.path_unpacked:
                    self.path_unpacked = (self.path_unpacked
                                          .rstrip("_archival_pdf"))
                    ZipFile(path).extractall(join(self.path_unpacked,
                                                  "archival_pdfs"))
                else:
                    ZipFile(path).extractall(self.path_unpacked)
                #TarFile.open(path).extractall(self.path_unpacked)
            except Exception:
                register_exception(alert_admin=True,
                                   prefix="OUP error extracting package.")
                self.logger.error("Error extraction package file: %s"
                                  % (path,))

        if hasattr(self, "path_unpacked"):
            return self.path_unpacked