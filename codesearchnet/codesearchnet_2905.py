def get_listing(path):
  """
  Returns the list of files and directories in a path.
  Prepents a ".." (parent directory link) if path is not current dir.
  """
  if path != ".":
    listing = sorted(['..'] + os.listdir(path))
  else:
    listing = sorted(os.listdir(path))
  return listing