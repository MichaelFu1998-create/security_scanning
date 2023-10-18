def put(self, key):
        """Put and return the only unique identifier possible, its url
        """
        self._consul_request('PUT', self._key_url(key['name']), json=key)
        return key['name']