def _ExpandDirectories(filenames):
  """Searches a list of filenames and replaces directories in the list with
  all files descending from those directories. Files with extensions not in
  the valid extensions list are excluded.

  Args:
    filenames: A list of files or directories

  Returns:
    A list of all files that are members of filenames or descended from a
    directory in filenames
  """
  expanded = set()
  for filename in filenames:
      if not os.path.isdir(filename):
        expanded.add(filename)
        continue

      for root, _, files in os.walk(filename):
        for loopfile in files:
          fullname = os.path.join(root, loopfile)
          if fullname.startswith('.' + os.path.sep):
            fullname = fullname[len('.' + os.path.sep):]
          expanded.add(fullname)

  filtered = []
  for filename in expanded:
      if os.path.splitext(filename)[1][1:] in GetAllExtensions():
          filtered.append(filename)

  return filtered