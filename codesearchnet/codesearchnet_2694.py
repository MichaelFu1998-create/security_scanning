def save_file(self, obj): # pylint: disable=too-many-branches
    """Save a file"""
    try:
      import StringIO as pystringIO #we can't use cStringIO as it lacks the name attribute
    except ImportError:
      import io as pystringIO # pylint: disable=reimported

    if not hasattr(obj, 'name') or  not hasattr(obj, 'mode'):
      raise pickle.PicklingError("Cannot pickle files that do not map to an actual file")
    if obj is sys.stdout:
      return self.save_reduce(getattr, (sys, 'stdout'), obj=obj)
    if obj is sys.stderr:
      return self.save_reduce(getattr, (sys, 'stderr'), obj=obj)
    if obj is sys.stdin:
      raise pickle.PicklingError("Cannot pickle standard input")
    if  hasattr(obj, 'isatty') and obj.isatty():
      raise pickle.PicklingError("Cannot pickle files that map to tty objects")
    if 'r' not in obj.mode:
      raise pickle.PicklingError("Cannot pickle files that are not opened for reading")
    name = obj.name
    try:
      fsize = os.stat(name).st_size
    except OSError:
      raise pickle.PicklingError("Cannot pickle file %s as it cannot be stat" % name)

    if obj.closed:
      #create an empty closed string io
      retval = pystringIO.StringIO("")
      retval.close()
    elif not fsize: #empty file
      retval = pystringIO.StringIO("")
      try:
        tmpfile = file(name)
        tst = tmpfile.read(1)
      except IOError:
        raise pickle.PicklingError("Cannot pickle file %s as it cannot be read" % name)
      tmpfile.close()
      if tst != '':
        raise pickle.PicklingError(
            "Cannot pickle file %s as it does not appear to map to a physical, real file" % name)
    else:
      try:
        tmpfile = file(name)
        contents = tmpfile.read()
        tmpfile.close()
      except IOError:
        raise pickle.PicklingError("Cannot pickle file %s as it cannot be read" % name)
      retval = pystringIO.StringIO(contents)
      curloc = obj.tell()
      retval.seek(curloc)

    retval.name = name
    self.save(retval)
    self.memoize(obj)