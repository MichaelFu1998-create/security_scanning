def valid_java_classpath(classpath):
  '''
  Given a java classpath, check whether the path entries are valid or not
  '''
  paths = classpath.split(':')
  for path_entry in paths:
    if not valid_path(path_entry.strip()):
      return False
  return True