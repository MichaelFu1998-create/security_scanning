def format_mode(sres):
  """
  Format a line in the directory list based on the file's type and other attributes.
  """
  mode = sres.st_mode

  root = (mode & 0o700) >> 6
  group = (mode & 0o070) >> 3
  user = (mode & 0o7)

  def stat_type(md):
    ''' stat type'''
    if stat.S_ISDIR(md):
      return 'd'
    elif stat.S_ISSOCK(md):
      return 's'
    else:
      return '-'

  def triple(md):
    ''' triple '''
    return '%c%c%c' % (
        'r' if md & 0b100 else '-',
        'w' if md & 0b010 else '-',
        'x' if md & 0b001 else '-')

  return ''.join([stat_type(mode), triple(root), triple(group), triple(user)])