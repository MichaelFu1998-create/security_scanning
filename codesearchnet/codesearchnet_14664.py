def load(self, origin_passphrase, keys=None, key_file=None):
        """Import keys to the stash from either a list of keys or a file

        `keys` is a list of dictionaries created by `self.export`
        `stash_path` is a path to a file created by `self.export`
        """
        # TODO: Handle keys not dict or key_file not json
        self._assert_valid_stash()

        # Check if both or none are provided (ahh, the mighty xor)
        if not (bool(keys) ^ bool(key_file)):
            raise GhostError(
                'You must either provide a path to an exported stash file '
                'or a list of key dicts to import')
        if key_file:
            with open(key_file) as stash_file:
                keys = json.loads(stash_file.read())

        # If the passphrases are the same, there's no reason to decrypt
        # and re-encrypt. We can simply pass the value.
        decrypt = origin_passphrase != self.passphrase
        if decrypt:
            # TODO: The fact that we need to create a stub stash just to
            # decrypt means we should probably have some encryptor class.
            stub = Stash(TinyDBStorage('stub'), origin_passphrase)
        # TODO: Handle existing keys when loading
        for key in keys:
            self.put(
                name=key['name'],
                value=stub._decrypt(key['value']) if decrypt else key['value'],
                metadata=key['metadata'],
                description=key['description'],
                lock=key.get('lock'),
                key_type=key.get('type'),
                encrypt=decrypt)