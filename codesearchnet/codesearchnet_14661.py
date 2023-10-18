def delete(self, key_name):
        """Delete a key if it exists.
        """
        self._assert_valid_stash()

        if key_name == 'stored_passphrase':
            raise GhostError(
                '`stored_passphrase` is a reserved ghost key name '
                'which cannot be deleted')

        # TODO: Optimize. We get from the storage twice here for no reason
        if not self.get(key_name):
            raise GhostError('Key `{0}` not found'.format(key_name))
        key = self._storage.get(key_name)
        if key.get('lock'):
            raise GhostError(
                'Key `{0}` is locked and therefore cannot be deleted '
                'Please unlock the key and try again'.format(key_name))

        deleted = self._storage.delete(key_name)

        audit(
            storage=self._storage.db_path,
            action='DELETE',
            message=json.dumps(dict(key_name=key_name)))

        if not deleted:
            raise GhostError('Failed to delete {0}'.format(key_name))