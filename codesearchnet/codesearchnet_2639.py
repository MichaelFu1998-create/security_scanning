def import_and_get_class(path_to_pex, python_class_name):
  """Imports and load a class from a given pex file path and python class name

  For example, if you want to get a class called `Sample` in
  /some-path/sample.pex/heron/examples/src/python/sample.py,
  ``path_to_pex`` needs to be ``/some-path/sample.pex``, and
  ``python_class_name`` needs to be ``heron.examples.src.python.sample.Sample``
  """
  abs_path_to_pex = os.path.abspath(path_to_pex)

  Log.debug("Add a pex to the path: %s" % abs_path_to_pex)
  Log.debug("In import_and_get_class with cls_name: %s" % python_class_name)
  split = python_class_name.split('.')
  from_path = '.'.join(split[:-1])
  import_name = python_class_name.split('.')[-1]

  Log.debug("From path: %s, import name: %s" % (from_path, import_name))

  # Resolve duplicate package suffix problem (heron.), if the top level package name is heron
  if python_class_name.startswith("heron."):
    try:
      mod = resolve_heron_suffix_issue(abs_path_to_pex, python_class_name)
      return getattr(mod, import_name)
    except:
      Log.error("Could not resolve class %s with special handling" % python_class_name)

  mod = __import__(from_path, fromlist=[import_name], level=-1)
  Log.debug("Imported module: %s" % str(mod))
  return getattr(mod, import_name)