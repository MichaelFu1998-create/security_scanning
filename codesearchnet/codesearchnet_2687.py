def _modules_to_main(modList):
  """Force every module in modList to be placed into main"""
  if not modList:
    return

  main = sys.modules['__main__']
  for modname in modList:
    if isinstance(modname, str):
      try:
        mod = __import__(modname)
      except Exception:
        sys.stderr.write(
            'warning: could not import %s\n.  '
            'Your function may unexpectedly error due to this import failing;'
            'A version mismatch is likely.  Specific error was:\n' % modname)
        print_exec(sys.stderr)
      else:
        setattr(main, mod.__name__, mod)