def _rc_keys(self, pattern='*'):
        "Returns a list of keys matching ``pattern``"

        result = []
        for alias, redisent in iteritems(self.redises):
            if alias.find('_slave') == -1:
                continue

            result.extend(redisent.keys(pattern))

        return result