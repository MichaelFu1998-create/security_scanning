def tail(filename, n):
  """Returns last n lines from the filename. No exception handling"""
  size = os.path.getsize(filename)
  with open(filename, "rb") as f:
   fm = mmap.mmap(f.fileno(), 0, mmap.MAP_SHARED, mmap.PROT_READ)
   try:
      for i in xrange(size - 1, -1, -1):
          if fm[i] == '\n':
             n -= 1
             if n == -1:
                break
      return fm[i + 1 if i else 0:].splitlines()
   finally:
        fm.close()