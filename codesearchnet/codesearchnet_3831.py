def tryload(self, cfgstr=None, on_error='raise'):
        """
        Like load, but returns None if the load fails due to a cache miss.

        Args:
            on_error (str): How to handle non-io errors errors. Either raise,
                which re-raises the exception, or clear which deletes the cache
                and returns None.
        """
        cfgstr = self._rectify_cfgstr(cfgstr)
        if self.enabled:
            try:
                if self.verbose > 1:
                    self.log('[cacher] tryload fname={}'.format(self.fname))
                return self.load(cfgstr)
            except IOError:
                if self.verbose > 0:
                    self.log('[cacher] ... {} cache miss'.format(self.fname))
            except Exception:
                if self.verbose > 0:
                    self.log('[cacher] ... failed to load')
                if on_error == 'raise':
                    raise
                elif on_error == 'clear':
                    self.clear(cfgstr)
                    return None
                else:
                    raise KeyError('Unknown method on_error={}'.format(on_error))
        else:
            if self.verbose > 1:
                self.log('[cacher] ... cache disabled: fname={}'.format(self.fname))
        return None