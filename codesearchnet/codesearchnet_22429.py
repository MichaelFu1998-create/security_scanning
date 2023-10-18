def _exists(self, path):
    '''IMPORTANT: expects `path` to already be deref()'erenced.'''
    try:
      return bool(self._stat(path))
    except os.error:
      return False