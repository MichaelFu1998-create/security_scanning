def clear(cls, persistent=False):
    """ If persistent is True, delete the temporary file

    Parameters:
    ----------------------------------------------------------------
    persistent: if True, custom configuration file is deleted
    """
    if persistent:
      try:
        os.unlink(cls.getPath())
      except OSError, e:
        if e.errno != errno.ENOENT:
          _getLogger().exception("Error %s while trying to remove dynamic " \
                                 "configuration file: %s", e.errno,
                                 cls.getPath())
          raise
    cls._path = None