def fso_listdir(self, path):
    'overlays os.listdir()'
    path = self.deref(path)
    if not stat.S_ISDIR(self._stat(path).st_mode):
      raise OSError(20, 'Not a directory', path)
    try:
      ret = self.originals['os:listdir'](path)
    except Exception:
      # assuming that `path` was created within this FSO...
      ret = []
    for entry in self.entries.values():
      if not entry.path.startswith(path + '/'):
        continue
      subpath = entry.path[len(path) + 1:]
      if '/' in subpath:
        continue
      if entry.mode is None:
        if subpath in ret:
          ret.remove(subpath)
      else:
        if subpath not in ret:
          ret.append(subpath)
    return ret