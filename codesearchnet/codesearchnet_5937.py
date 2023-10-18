def get_stats(self):
        """Get general stats for the cache."""
        expired = sum([x['expired'] for _, x in
                       self._CACHE_STATS['access_stats'].items()])
        miss = sum([x['miss'] for _, x in
                    self._CACHE_STATS['access_stats'].items()])

        hit = sum([x['hit'] for _, x in
                       self._CACHE_STATS['access_stats'].items()])
        return {
            'totals': {
                'keys': len(self._CACHE_STATS['access_stats']),
                'expired': expired,
                'miss': miss,
                'hit': hit,
                }
        }