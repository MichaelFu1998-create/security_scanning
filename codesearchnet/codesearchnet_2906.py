def get_stat(path, filename):
  ''' get stat '''
  return os.stat(os.path.join(path, filename))