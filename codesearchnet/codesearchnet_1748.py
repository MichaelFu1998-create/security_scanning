def pack(fmt, *args):
  """pack(fmt, v1, v2, ...) -> string
     Return string containing values v1, v2, ... packed according to fmt.
     See struct.__doc__ for more on format strings."""
  formatdef, endianness, i = getmode(fmt)
  args = list(args)
  n_args = len(args)
  result = []
  while i < len(fmt):
    num, i = getNum(fmt, i)
    cur = fmt[i]
    try:
      format = formatdef[cur]
    except KeyError:
      raise StructError("%s is not a valid format" % cur)
    if num == None:
      num_s = 0
      num = 1
    else:
      num_s = num

    if cur == 'x':
      result += [b'\0' * num]
    elif cur == 's':
      if isinstance(args[0], bytes):
        padding = num - len(args[0])
        result += [args[0][:num] + b'\0' * padding]
        args.pop(0)
      else:
        raise StructError("arg for string format not a string")
    elif cur == 'p':
      if isinstance(args[0], bytes):
        padding = num - len(args[0]) - 1

        if padding > 0:
          result += [bytes([len(args[0])]) + args[0]
                     [:num - 1] + b'\0' * padding]
        else:
          if num < 255:
            result += [bytes([num - 1]) + args[0][:num - 1]]
          else:
            result += [bytes([255]) + args[0][:num - 1]]
        args.pop(0)
      else:
        raise StructError("arg for string format not a string")

    else:
      if len(args) < num:
        raise StructError("insufficient arguments to pack")
      for var in args[:num]:
        result += [format['pack'](var, format['size'], endianness)]
      args = args[num:]
    num = None
    i += 1
  if len(args) != 0:
    raise StructError("too many arguments for pack format")
  return b''.join(result)