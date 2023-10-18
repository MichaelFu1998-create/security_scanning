def _read_version(self, data):
        '''Read header version from data'''

        version = ord(data[0])
        if version not in self.VERSIONS:
            raise Exception('Version not defined: %d' % version)
        return version