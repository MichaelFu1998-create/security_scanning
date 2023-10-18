def create_or_update_kv2(self, path, data, cas=None, mount_path='secret'):
        """
        Create or update some data in a key/value version 2 secret engine.

        :raises CasError:
            Raises an error if the ``cas`` value, when provided, doesn't match
            Vault's version for the key.
        """
        params = {
            'options': {},
            'data': data
        }
        if cas is not None:
            params['options']['cas'] = cas

        write_path = '{}/data/{}'.format(mount_path, path)
        return self.write(write_path, **params)