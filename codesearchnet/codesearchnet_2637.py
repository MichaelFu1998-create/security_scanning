def load_pex(path_to_pex, include_deps=True):
  """Loads pex file and its dependencies to the current python path"""
  abs_path_to_pex = os.path.abspath(path_to_pex)
  Log.debug("Add a pex to the path: %s" % abs_path_to_pex)
  if abs_path_to_pex not in sys.path:
    sys.path.insert(0, os.path.dirname(abs_path_to_pex))

  # add dependencies to path
  if include_deps:
    for dep in _get_deps_list(abs_path_to_pex):
      to_join = os.path.join(os.path.dirname(abs_path_to_pex), dep)
      if to_join not in sys.path:
        Log.debug("Add a new dependency to the path: %s" % dep)
        sys.path.insert(0, to_join)

  Log.debug("Python path: %s" % str(sys.path))