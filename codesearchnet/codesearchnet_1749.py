def unpack(fmt, data):
  """unpack(fmt, string) -> (v1, v2, ...)
     Unpack the string, containing packed C structure data, according
     to fmt.  Requires len(string)==calcsize(fmt).
     See struct.__doc__ for more on format strings."""
  formatdef, endianness, i = getmode(fmt)
  j = 0
  num = 0
  result = []
  length = calcsize(fmt)
  if length != len(data):
    raise StructError("unpack str size does not match format")
  while i < len(fmt):
    num, i = getNum(fmt, i)
    cur = fmt[i]
    i += 1
    try:
      format = formatdef[cur]
    except KeyError:
      raise StructError("%s is not a valid format" % cur)

    if not num:
      num = 1

    if cur == 'x':
      j += num
    elif cur == 's':
      result.append(data[j:j + num])
      j += num
    elif cur == 'p':
      n = data[j]
      if n >= num:
        n = num - 1
      result.append(data[j + 1:j + n + 1])
      j += num
    else:
      for n in range(num):
        result += [format['unpack'](data, j, format['size'], endianness)]
        j += format['size']

  return tuple(result)