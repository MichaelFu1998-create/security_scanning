def include(f):
  '''
  includes the contents of a file on disk.
  takes a filename
  '''
  fl = open(f, 'r')
  data = fl.read()
  fl.close()
  return raw(data)