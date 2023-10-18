def load(cls, stream, contentType=None, version=None):
    '''
    Reverses the effects of the :meth:`dump` method, creating a FileItem
    from the specified file-like `stream` object.
    '''
    if contentType is None:
      contentType = constants.TYPE_OMADS_FILE
    if ctype.getBaseType(contentType) == constants.TYPE_OMADS_FOLDER:
      from .folder import FolderItem
      return FolderItem.load(stream, contentType, version)
    if ctype.getBaseType(contentType) != constants.TYPE_OMADS_FILE:
      raise common.InvalidContentType('cannot de-serialize FileItem from "%s"' % (contentType,))
    if version is None:
      version = '1.2'
    if version != '1.2':
      raise common.InvalidContentType('invalid FileItem de-serialization version "%s"' % (version,))
    ret = FileItem()
    data = stream.read()
    xdoc = ET.fromstring(data)
    if xdoc.tag != 'File':
      raise common.InvalidContent('root of application/vnd.omads-file XML must be "File" not "%s"'
                                  % (xdoc.tag,))
    ret.name = xdoc.findtext('name')
    ret.body = xdoc.findtext('body')
    ret.size = xdoc.findtext('size')
    if ret.body is not None:
      ret.size = len(ret.body)
    elif ret.size is not None:
      ret.size = int(ret.size)
    # todo: do anything with "parent"?...
    # load the date attributes
    for attr in ('created', 'modified', 'accessed'):
      val = xdoc.findtext(attr)
      if val is not None:
        setattr(ret, attr, int(common.parse_ts_iso(val)))
    # load the boolean attributes
    for attr in ('hidden', 'system', 'archived', 'delete',
                 'writable', 'readable', 'executable'):
      val = xdoc.findtext('attributes/' + attr[0])
      if val is not None:
        setattr(ret, attr, val.lower() == 'true')
    return ret