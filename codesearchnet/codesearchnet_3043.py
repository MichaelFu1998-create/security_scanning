def pick(dirname, pattern):
  '''
  Get the topology jars
  :param dirname:
  :param pattern:
  :return:
  '''
  file_list = fnmatch.filter(os.listdir(dirname), pattern)
  return file_list[0] if file_list else None