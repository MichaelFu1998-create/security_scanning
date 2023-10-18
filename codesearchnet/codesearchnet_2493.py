def get_heron_dir():
  """
  This will extract heron directory from .pex file.

  For example,
  when __file__ is '/Users/heron-user/bin/heron/heron/tools/common/src/python/utils/config.pyc', and
  its real path is '/Users/heron-user/.heron/bin/heron/tools/common/src/python/utils/config.pyc',
  the internal variable ``path`` would be '/Users/heron-user/.heron', which is the heron directory

  This means the variable `go_above_dirs` below is 9.

  :return: root location of the .pex file
  """
  go_above_dirs = 9
  path = "/".join(os.path.realpath(__file__).split('/')[:-go_above_dirs])
  return normalized_class_path(path)