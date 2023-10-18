def get(self, key_name, decrypt=True):
        """Return a key with its parameters if it was found.
        """
        self._assert_valid_stash()

        key = self._storage.get(key_name).copy()
        if not key.get('value'):
            return None
        if decrypt:
            key['value'] = self._decrypt(key['value'])

        audit(
            storage=self._storage.db_path,
            action='GET',
            message=json.dumps(dict(key_name=key_name)))

        return key