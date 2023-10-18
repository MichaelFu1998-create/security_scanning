def check_file(self, filename):
        # type: (str) -> bool
        """
        Check if ``filename`` can be read. Will return boolean which is True if
        the file can be read, False otherwise.
        """
        if not exists(filename):
            return False

        # Check if the file is version-compatible with this instance.
        new_config = ConfigResolverBase()
        new_config.read(filename)
        if self.version and not new_config.has_option('meta', 'version'):
            # self.version is set, so we MUST have a version in the file!
            raise NoVersionError(
                "The config option 'meta.version' is missing in {}. The "
                "application expects version {}!".format(filename,
                                                         self.version))
        elif not self.version and new_config.has_option('meta', 'version'):
            # Automatically "lock-in" a version number if one is found.
            # This prevents loading a chain of config files with incompatible
            # version numbers!
            self.version = StrictVersion(new_config.get('meta', 'version'))
            self._log.info('%r contains a version number, but the config '
                           'instance was not created with a version '
                           'restriction. Will set version number to "%s" to '
                           'prevent accidents!',
                           filename, self.version)
        elif self.version:
            # This instance expected a certain version. We need to check the
            # version in the file and compare.
            file_version = new_config.get('meta', 'version')
            major, minor, _ = StrictVersion(file_version).version
            expected_major, expected_minor, _ = self.version.version
            if expected_major != major:
                self._log.error(
                    'Invalid major version number in %r. Expected %r, got %r!',
                    abspath(filename),
                    str(self.version),
                    file_version)
                return False

            if expected_minor != minor:
                self._log.warning(
                    'Mismatching minor version number in %r. '
                    'Expected %r, got %r!',
                    abspath(filename),
                    str(self.version),
                    file_version)
                return True
        return True