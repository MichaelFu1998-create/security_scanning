def get_heron_tracker_dir():
  """
  This will extract heron tracker directory from .pex file.
  :return: root location for heron-tools.
  """
  path = "/".join(os.path.realpath(__file__).split('/')[:-8])
  return normalized_class_path(path)