def _openStream(dataUrl,
                  isBlocking,  # pylint: disable=W0613
                  maxTimeout,  # pylint: disable=W0613
                  bookmark,
                  firstRecordIdx):
    """Open the underlying file stream
    This only supports 'file://' prefixed paths.

    :returns: record stream instance
    :rtype: FileRecordStream
    """
    filePath = dataUrl[len(FILE_PREF):]
    if not os.path.isabs(filePath):
      filePath = os.path.join(os.getcwd(), filePath)
    return FileRecordStream(streamID=filePath,
                            write=False,
                            bookmark=bookmark,
                            firstRecord=firstRecordIdx)