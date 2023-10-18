def get_all(self, key=None):
        '''
        Returns all data entries for a particular key. Default is the main key.

        Args:

            key (str): key whose values to return (default: main key)

        Returns:

            List of all data entries for the key
        '''
        key = self.definition.main_key if key is None else key
        key = self.definition.key_synonyms.get(key, key)
        entries = self._get_all(key)
        if key in self.definition.scalar_nonunique_keys:
            return set(entries)
        return entries