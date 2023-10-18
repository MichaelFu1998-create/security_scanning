def fso_exists(self, path):
    'overlays os.path.exists()'
    try:
      return self._exists(self.deref(path))
    except os.error:
      return False