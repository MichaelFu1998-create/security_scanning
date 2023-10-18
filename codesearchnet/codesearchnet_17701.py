def get(self, key, default=None):
        """ Get key value, return default if key doesn't exist """
        if self.in_memory:
            return self._memory_db.get(key, default)
        else:
            db = self._read_file()
            return db.get(key, default)