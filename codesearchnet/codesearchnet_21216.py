def dump(self, stream, contentType=None, version=None):
    '''
    Serializes this NoteItem to a byte-stream and writes it to the
    file-like object `stream`. `contentType` and `version` must be one
    of the supported content-types, and if not specified, will default
    to ``text/plain``.
    '''
    if contentType is None or contentType == constants.TYPE_TEXT_PLAIN:
      stream.write(self.body)
      return
    if contentType == constants.TYPE_SIF_NOTE:
      root = ET.Element('note')
      # TODO: check `version`...
      ET.SubElement(root, 'SIFVersion').text = '1.1'
      if self.name is not None:
        ET.SubElement(root, 'Subject').text = self.name
      if self.body is not None:
        ET.SubElement(root, 'Body').text = self.body
      for name, values in self.extensions.items():
        for value in values:
          ET.SubElement(root, name).text = value
      ET.ElementTree(root).write(stream)
      return
    raise common.InvalidContentType('cannot serialize NoteItem to "%s"' % (contentType,))