def put(self, key):
        """Put and return the only unique identifier possible, its path
        """
        self.client.write(self._key_path(key['name']), **key)
        return self._key_path(key['name'])