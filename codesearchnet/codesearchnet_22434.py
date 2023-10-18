def fso_mkdir(self, path, mode=None):
    'overlays os.mkdir()'
    path = self.deref(path, to_parent=True)
    if self._lexists(path):
      raise OSError(17, 'File exists', path)
    self._addentry(OverlayEntry(self, path, stat.S_IFDIR))