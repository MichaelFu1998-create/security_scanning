def _stat(self, path):
    '''IMPORTANT: expects `path`'s parent to already be deref()'erenced.'''
    if path not in self.entries:
      return OverlayStat(*self.originals['os:stat'](path)[:10], st_overlay=0)
    st = self.entries[path].stat
    if stat.S_ISLNK(st.st_mode):
      return self._stat(self.deref(path))
    return st