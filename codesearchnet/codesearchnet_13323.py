def prepare(self, data):
        """Complete string preparation procedure for 'stored' strings.
        (includes checks for unassigned codes)

        :Parameters:
            - `data`: Unicode string to prepare.

        :return: prepared string

        :raise StringprepError: if the preparation fails
        """
        ret = self.cache.get(data)
        if ret is not None:
            return ret
        result = self.map(data)
        if self.normalization:
            result = self.normalization(result)
        result = self.prohibit(result)
        result = self.check_unassigned(result)
        if self.bidi:
            result = self.check_bidi(result)
        if isinstance(result, list):
            result = u"".join()
        if len(self.cache_items) >= _stringprep_cache_size:
            remove = self.cache_items[: -_stringprep_cache_size // 2]
            for profile, key in remove:
                try:
                    del profile.cache[key]
                except KeyError:
                    pass
            self.cache_items[:] = self.cache_items[
                                                -_stringprep_cache_size // 2 :]
        self.cache_items.append((self, data))
        self.cache[data] = result
        return result