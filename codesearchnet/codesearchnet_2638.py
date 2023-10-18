def resolve_heron_suffix_issue(abs_pex_path, class_path):
  """Resolves duplicate package suffix problems

  When dynamically loading a pex file and a corresponding python class (bolt/spout/topology),
  if the top level package in which to-be-loaded classes reside is named 'heron', the path conflicts
  with this Heron Instance pex package (heron.instance.src.python...), making the Python
  interpreter unable to find the target class in a given pex file.
  This function resolves this issue by individually loading packages with suffix `heron` to
  avoid this issue.

  However, if a dependent module/class that is not directly specified under ``class_path``
  and has conflicts with other native heron packages, there is a possibility that
  such a class/module might not be imported correctly. For example, if a given ``class_path`` was
  ``heron.common.src.module.Class``, but it has a dependent module (such as by import statement),
  ``heron.common.src.python.dep_module.DepClass`` for example, pex_loader does not guarantee that
  ``DepClass` is imported correctly. This is because ``heron.common.src.python.dep_module`` is not
  explicitly added to sys.path, while ``heron.common.src.python`` module exists as the native heron
  package, from which ``dep_module`` cannot be found, so Python interpreter may raise ImportError.

  The best way to avoid this issue is NOT to dynamically load a pex file whose top level package
  name is ``heron``. Note that this method is included because some of the example topologies and
  tests have to have a pex with its top level package name of ``heron``.
  """
  # import top-level package named `heron` of a given pex file
  importer = zipimport.zipimporter(abs_pex_path)
  importer.load_module("heron")

  # remove 'heron' and the classname
  to_load_lst = class_path.split('.')[1:-1]
  loaded = ['heron']
  loaded_mod = None
  for to_load in to_load_lst:
    sub_importer = zipimport.zipimporter(os.path.join(abs_pex_path, '/'.join(loaded)))
    loaded_mod = sub_importer.load_module(to_load)
    loaded.append(to_load)

  return loaded_mod