def get_heron_libs(local_jars):
  """Get all the heron lib jars with the absolute paths"""
  heron_lib_dir = get_heron_lib_dir()
  heron_libs = [os.path.join(heron_lib_dir, f) for f in local_jars]
  return heron_libs