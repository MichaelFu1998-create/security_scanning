def calcsize(fmt):
  """calcsize(fmt) -> int
  Return size of C struct described by format string fmt.
  See struct.__doc__ for more on format strings."""

  formatdef, endianness, i = getmode(fmt)
  num = 0
  result = 0
  while i < len(fmt):
    num, i = getNum(fmt, i)
    cur = fmt[i]
    try:
      format = formatdef[cur]
    except KeyError:
      raise StructError("%s is not a valid format" % cur)
    if num != None:
      result += num * format['size']
    else:
      result += format['size']
    num = 0
    i += 1
  return result