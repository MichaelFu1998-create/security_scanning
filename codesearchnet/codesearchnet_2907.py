def read_chunk(filename, offset=-1, length=-1, escape_data=False):
  """
  Read a chunk of a file from an offset upto the length.
  """
  try:
    length = int(length)
    offset = int(offset)
  except ValueError:
    return {}

  if not os.path.isfile(filename):
    return {}

  try:
    fstat = os.stat(filename)
  except Exception:
    return {}

  if offset == -1:
    offset = fstat.st_size

  if length == -1:
    length = fstat.st_size - offset

  with open(filename, "r") as fp:
    fp.seek(offset)
    try:
      data = fp.read(length)
    except IOError:
      return {}

  if data:
    data = _escape_data(data) if escape_data else data
    return dict(offset=offset, length=len(data), data=data)

  return dict(offset=offset, length=0)