def go_str(value):
  """Returns value as a valid Go string literal."""
  io = StringIO.StringIO()
  io.write('"')
  for c in value:
    if c in _ESCAPES:
      io.write(_ESCAPES[c])
    elif c in _SIMPLE_CHARS:
      io.write(c)
    else:
      io.write(r'\x{:02x}'.format(ord(c)))
  io.write('"')
  return io.getvalue()