def fso_rmdir(self, path):
    'overlays os.rmdir()'
    st = self.fso_lstat(path)
    if not stat.S_ISDIR(st.st_mode):
      raise OSError(20, 'Not a directory', path)
    if len(self.fso_listdir(path)) > 0:
      raise OSError(39, 'Directory not empty', path)
    self._addentry(OverlayEntry(self, path, None))