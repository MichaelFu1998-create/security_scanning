def _lexists(self, path):
    '''IMPORTANT: expects `path` to already be deref()'erenced.'''
    try:
      return bool(self._lstat(path))
    except os.error:
      return False