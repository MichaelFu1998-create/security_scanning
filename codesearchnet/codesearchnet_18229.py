def _remove_by_pk(self, key, flush=True):
        """Retrieve value from store.

        :param key: Key

        """
        try:
            del self.store[key]
        except Exception as error:
            pass
        if flush:
            self.flush()