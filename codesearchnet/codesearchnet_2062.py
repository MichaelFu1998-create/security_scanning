def calculate_transitive_deps(modname, script, gopath):
  """Determines all modules that script transitively depends upon."""
  deps = set()
  def calc(modname, script):
    if modname in deps:
      return
    deps.add(modname)
    for imp in collect_imports(modname, script, gopath):
      if imp.is_native:
        deps.add(imp.name)
        continue
      parts = imp.name.split('.')
      calc(imp.name, imp.script)
      if len(parts) == 1:
        continue
      # For submodules, the parent packages are also deps.
      package_dir, filename = os.path.split(imp.script)
      if filename == '__init__.py':
        package_dir = os.path.dirname(package_dir)
      for i in xrange(len(parts) - 1, 0, -1):
        modname = '.'.join(parts[:i])
        script = os.path.join(package_dir, '__init__.py')
        calc(modname, script)
        package_dir = os.path.dirname(package_dir)
  calc(modname, script)
  deps.remove(modname)
  return deps