def fso_readlink(self, path):
    'overlays os.readlink()'
    path = self.deref(path, to_parent=True)
    st = self.fso_lstat(path)
    if not stat.S_ISLNK(st.st_mode):
      raise OSError(22, 'Invalid argument', path)
    if st.st_overlay:
      return self.entries[path].content
    return self.originals['os:readlink'](path)