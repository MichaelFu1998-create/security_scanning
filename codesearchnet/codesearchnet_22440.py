def fso_islink(self, path):
    'overlays os.path.islink()'
    try:
      return stat.S_ISLNK(self.fso_lstat(path).st_mode)
    except OSError:
      return False