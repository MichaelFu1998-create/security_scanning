def object(self, infotype, key):
        "Return the encoding, idletime, or refcount about the key"
        redisent = self.redises[self._getnodenamefor(key) + '_slave']
        return getattr(redisent, 'object')(infotype, key)