def _FilterExcludedFiles(filenames):
  """Filters out files listed in the --exclude command line switch. File paths
  in the switch are evaluated relative to the current working directory
  """
  exclude_paths = [os.path.abspath(f) for f in _excludes]
  return [f for f in filenames if os.path.abspath(f) not in exclude_paths]