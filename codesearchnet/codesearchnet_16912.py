def _assert_version(self, version):
        '''
        Assert that the grid version is equal to or above the given value.
        If no version is set, set the version.
        '''
        if self.nearest_version < version:
            if self._version_given:
                raise ValueError(
                        'Data type requires version %s' \
                        % version)
            else:
                self._version = version