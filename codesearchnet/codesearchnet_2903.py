def format_mtime(mtime):
  """
  Format the date associated with a file to be displayed in directory listing.
  """
  now = datetime.now()
  dt = datetime.fromtimestamp(mtime)
  return '%s %2d %5s' % (
      dt.strftime('%b'), dt.day,
      dt.year if dt.year != now.year else dt.strftime('%H:%M'))