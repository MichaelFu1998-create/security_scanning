def _lstat(self, path):
    '''IMPORTANT: expects `path`'s parent to already be deref()'erenced.'''
    if path not in self.entries:
      return OverlayStat(*self.originals['os:lstat'](path)[:10], st_overlay=0)
    return self.entries[path].stat