def normalizeStreamSource(self, stream):
    """
    TODO: document
    :param stream:
    """
    # The stream source in the task might be in several formats, so we need
    # to make sure it gets converted into an absolute path:
    source = stream['source'][len(FILE_SCHEME):]
    # If the source is already an absolute path, we won't use pkg_resources,
    # we'll just trust that the path exists. If not, it's a user problem.
    if os.path.isabs(source):
      sourcePath = source
    else:
      # First we'll check to see if this path exists within the nupic.datafiles
      # package resource.
      sourcePath = resource_filename("nupic.datafiles", source)
      if not os.path.exists(sourcePath):
        # If this path doesn't exist as a package resource, the last option will
        # be to treat it as a relative path to the current working directory.
        sourcePath = os.path.join(os.getcwd(), source)
    stream['source'] = FILE_SCHEME + sourcePath