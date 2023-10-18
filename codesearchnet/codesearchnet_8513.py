def contains_key(self, *keys):
        """Asserts the val is a dict and contains the given key or keys.  Alias for contains()."""
        self._check_dict_like(self.val, check_values=False, check_getitem=False)
        return self.contains(*keys)