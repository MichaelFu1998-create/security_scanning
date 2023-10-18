def fso_unlink(self, path):
    'overlays os.unlink()'
    path = self.deref(path, to_parent=True)
    if not self._lexists(path):
      raise OSError(2, 'No such file or directory', path)
    self._addentry(OverlayEntry(self, path, None))