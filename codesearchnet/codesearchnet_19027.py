def _rc_dbsize(self):
        "Returns the number of keys in the current database"

        result = 0
        for alias, redisent in iteritems(self.redises):
            if alias.find('_slave') == -1:
                continue

            result += redisent.dbsize()

        return result