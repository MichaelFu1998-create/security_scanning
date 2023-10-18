def get_namespace_hash(self, hash_fn=hashlib.md5) -> str:
        """Get the namespace hash.

        Defaults to MD5.
        """
        m = hash_fn()

        if self.has_names:
            items = self._get_namespace_name_to_encoding(desc='getting hash').items()
        else:
            items = self._get_namespace_identifier_to_encoding(desc='getting hash').items()

        for name, encoding in items:
            m.update(f'{name}:{encoding}'.encode('utf8'))
        return m.hexdigest()