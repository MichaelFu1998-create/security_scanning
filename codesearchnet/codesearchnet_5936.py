def get_access_details(self, key=None):
        """Get access details in cache."""
        if key in self._CACHE_STATS:
            return self._CACHE_STATS['access_stats'][key]
        else:
            return self._CACHE_STATS['access_stats']