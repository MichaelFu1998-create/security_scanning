def fso_symlink(self, source, link_name):
    'overlays os.symlink()'
    path = self.deref(link_name, to_parent=True)
    if self._exists(path):
      raise OSError(17, 'File exists')
    self._addentry(OverlayEntry(self, path, stat.S_IFLNK, source))