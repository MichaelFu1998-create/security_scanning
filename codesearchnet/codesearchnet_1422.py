def readUserSession(datafile):
  """
  Reads the user session record from the file's cursor position
  Args:
    datafile: Data file whose cursor points at the beginning of the record

  Returns:
    list of pages in the order clicked by the user
  """
  for line in datafile:
    pages = line.split()
    total = len(pages)
    # Select user sessions with 2 or more pages
    if total < 2:
      continue

    # Exclude outliers by removing extreme long sessions
    if total > 500:
      continue

    return [PAGE_CATEGORIES[int(i) - 1] for i in pages]
  return []