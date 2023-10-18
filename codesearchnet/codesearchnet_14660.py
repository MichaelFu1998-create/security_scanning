def list(self,
             key_name=None,
             max_suggestions=100,
             cutoff=0.5,
             locked_only=False,
             key_type=None):
        """Return a list of all keys.
        """
        self._assert_valid_stash()

        key_list = [k for k in self._storage.list()
                    if k['name'] != 'stored_passphrase' and
                    (k.get('lock') if locked_only else True)]

        if key_type:
            # To maintain backward compatibility with keys without a type.
            # The default key type is secret, in which case we also look for
            # keys with no (None) types.
            types = ('secret', None) if key_type == 'secret' else [key_type]
            key_list = [k for k in key_list if k.get('type') in types]

        key_list = [k['name'] for k in key_list]
        if key_name:
            if key_name.startswith('~'):
                key_list = difflib.get_close_matches(
                    key_name.lstrip('~'), key_list, max_suggestions, cutoff)
            else:
                key_list = [k for k in key_list if key_name in k]

        audit(
            storage=self._storage.db_path,
            action='LIST' + ('[LOCKED]' if locked_only else ''),
            message=json.dumps(dict()))

        return key_list