def _fetch(self):
        """forces update of a local cached copy of the real object
        (regardless of the preference setting self.cache)"""
        if not self._obcache_current:
            from distob import engine
            ax = self._distaxis
            self._obcache = concatenate([ra._ob for ra in self._subarrays], ax)
            # let subarray obcaches and main obcache be views on same memory:
            for i in range(self._n):
                ix = [slice(None)] * self.ndim
                ix[ax] = slice(self._si[i], self._si[i+1])
                self._subarrays[i]._obcache = self._obcache[tuple(ix)]
            self._obcache_current = True
            # now prefer local processing:
            self.__engine_affinity__ = (
                    engine.eid, self.__engine_affinity__[1])