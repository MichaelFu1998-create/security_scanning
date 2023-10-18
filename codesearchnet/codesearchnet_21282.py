def dump(self, stream, contentType=None, version=None):
    '''
    Serializes this FileItem to a byte-stream and writes it to the
    file-like object `stream`. `contentType` and `version` must be one
    of the supported content-types, and if not specified, will default
    to ``application/vnd.omads-file``.
    '''
    if contentType is None:
      contentType = constants.TYPE_OMADS_FILE
    if ctype.getBaseType(contentType) != constants.TYPE_OMADS_FILE:
      raise common.InvalidContentType('cannot serialize FileItem to "%s"' % (contentType,))
    if version is None:
      version = '1.2'
    if version != '1.2':
      raise common.InvalidContentType('invalid file serialization version "%s"' % (version,))
    root = ET.Element('File')
    if self.name is not None:
      ET.SubElement(root, 'name').text = self.name
    # todo: do anything with "parent"?...
    for attr in ('created', 'modified', 'accessed'):
      if getattr(self, attr) is None:
        continue
      ET.SubElement(root, attr).text = common.ts_iso(getattr(self, attr))
    if self.contentType is not None:
      ET.SubElement(root, 'cttype').text = self.contentType
    attrs = [attr
             for attr in ('hidden', 'system', 'archived', 'delete', 'writable', 'readable', 'executable')
             if getattr(self, attr) is not None]
    if len(attrs) > 0:
      xa = ET.SubElement(root, 'attributes')
      for attr in attrs:
        ET.SubElement(xa, attr[0]).text = 'true' if getattr(self, attr) else 'false'
    if self.body is not None:
      ET.SubElement(root, 'body').text = self.body
    if self.body is None and self.size is not None:
      ET.SubElement(root, 'size').text = str(self.size)
    if len(self.extensions) > 0:
      xe = ET.SubElement(root, 'Ext')
      for name, values in self.extensions.items():
        ET.SubElement(xe, 'XNam').text = name
        for value in values:
          ET.SubElement(xe, 'XVal').text = value
    ET.ElementTree(root).write(stream)
    return (constants.TYPE_OMADS_FILE + '+xml', '1.2')