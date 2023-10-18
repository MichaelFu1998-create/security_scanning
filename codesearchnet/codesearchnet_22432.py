def fso_lexists(self, path):
    'overlays os.path.lexists()'
    try:
      return self._lexists(self.deref(path, to_parent=True))
    except os.error:
      return False