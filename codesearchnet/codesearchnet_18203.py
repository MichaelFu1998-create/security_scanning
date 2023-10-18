def read_kv2(self, path, version=None, mount_path='secret'):
        """
        Read some data from a key/value version 2 secret engine.
        """
        params = {}
        if version is not None:
            params['version'] = version

        read_path = '{}/data/{}'.format(mount_path, path)
        return self.read(read_path, **params)