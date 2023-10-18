def unescape(data):
  '''
  unescapes html entities. the opposite of escape.
  '''
  cc = re.compile(r'&(?:(?:#(\d+))|([^;]+));')

  result = []
  m = cc.search(data)
  while m:
    result.append(data[0:m.start()])
    d = m.group(1)
    if d:
      d = int(d)
      result.append(unichr(d))
    else:
      d = _unescape.get(m.group(2), ord('?'))
      result.append(unichr(d))

    data = data[m.end():]
    m = cc.search(data)

  result.append(data)
  return ''.join(result)