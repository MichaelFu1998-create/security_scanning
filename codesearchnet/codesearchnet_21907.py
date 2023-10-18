def _fetch(self):
        """forces update of a local cached copy of the real object
        (regardless of the preference setting self.cache)"""
        if not self.is_local and not self._obcache_current:
            #print('fetching data from %s' % self._ref.id)
            def _remote_fetch(id):
                return distob.engine[id]
            self._obcache = self._dv.apply_sync(_remote_fetch, self._id)
            self._obcache_current = True
            self.__engine_affinity__ = (distob.engine.eid, 
                                        self.__engine_affinity__[1])