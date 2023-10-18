def fso_makedirs(self, path, mode=None):
    'overlays os.makedirs()'
    path = self.abs(path)
    cur = '/'
    segments = path.split('/')
    for idx, seg in enumerate(segments):
      cur = os.path.join(cur, seg)
      try:
        st = self.fso_stat(cur)
      except OSError:
        st = None
      if st is None:
        self.fso_mkdir(cur)
        continue
      if idx + 1 == len(segments):
        raise OSError(17, 'File exists', path)
      if not stat.S_ISDIR(st.st_mode):
        raise OSError(20, 'Not a directory', path)