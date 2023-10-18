def purge(self, force=False, key_type=None):
        """Purge the stash from all keys
        """
        self._assert_valid_stash()

        if not force:
            raise GhostError(
                "The `force` flag must be provided to perform a stash purge. "
                "I mean, you don't really want to just delete everything "
                "without precautionary measures eh?")

        audit(
            storage=self._storage.db_path,
            action='PURGE',
            message=json.dumps(dict()))

        for key_name in self.list(key_type=key_type):
            self.delete(key_name)