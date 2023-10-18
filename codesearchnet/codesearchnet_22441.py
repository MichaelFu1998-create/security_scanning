def fso_rmtree(self, path, ignore_errors=False, onerror=None):
    'overlays shutil.rmtree()'
    if ignore_errors:
      def onerror(*args):
        pass
    elif onerror is None:
      def onerror(*args):
        raise
    try:
      if self.fso_islink(path):
        # symlinks to directories are forbidden, see shutil bug #1669
        raise OSError('Cannot call rmtree on a symbolic link')
    except OSError:
      onerror(os.path.islink, path, sys.exc_info())
      # can't continue even if onerror hook returns
      return
    names = []
    try:
      names = self.fso_listdir(path)
    except os.error, err:
      onerror(os.listdir, path, sys.exc_info())
    for name in names:
      fullname = os.path.join(path, name)
      try:
        mode = self.fso_lstat(fullname).st_mode
      except os.error:
        mode = 0
      if stat.S_ISDIR(mode):
        self.fso_rmtree(fullname, ignore_errors, onerror)
      else:
        try:
          self.fso_remove(fullname)
        except OSError as err:
          onerror(os.remove, fullname, sys.exc_info())
    try:
      self.fso_rmdir(path)
    except os.error:
      onerror(os.rmdir, path, sys.exc_info())