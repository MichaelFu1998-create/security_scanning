def _update_cache_stats(self, key, result):
        """
        Update the cache stats.
        
        If no cache-result is specified, we iniitialize the key.
        Otherwise, we increment the correct cache-result.

        Note the behavior for expired.  A client can be expired and the key
        still exists.
        """
        if result is None:
            self._CACHE_STATS['access_stats'].setdefault(key,
                                         {'hit': 0, 'miss': 0, 'expired': 0})
        else:
            self._CACHE_STATS['access_stats'][key][result] +=1