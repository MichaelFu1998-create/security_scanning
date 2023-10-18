def _extract_packages(self):
        """
        Extract a package in a new directory.
        """
        self.path_unpacked = []
        if not hasattr(self, "retrieved_packages_unpacked"):
            self.retrieved_packages_unpacked = [self.package_name]
        for path in self.retrieved_packages_unpacked:
            self.logger.debug("Extracting package: %s" % (path,))

            p_name = 'EPJC' if 'EPJC' in path else 'JHEP'
            p_message = 'scoap3_package_%s_%s_' % (p_name, datetime.now())

            self.path_unpacked.append(mkdtemp(prefix=p_message,
                                              dir=CFG_TMPSHAREDDIR))

            try:
                ZipFile(path).extractall(self.path_unpacked[-1])
            except Exception:
                register_exception(alert_admin=True,
                                   prefix="Springer error extracting package.")
                self.logger.error("Error extraction package file: %s"
                                  % (path,))

        return self.path_unpacked