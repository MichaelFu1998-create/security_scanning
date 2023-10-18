def load(cls, stream, contentType=None, version=None):
    '''
    Reverses the effects of the :meth:`dump` method, creating a NoteItem
    from the specified file-like `stream` object.
    '''
    if contentType is None or contentType == constants.TYPE_TEXT_PLAIN:
      data = stream.read()
      name = data.split('\n')[0]
      # todo: localize?!...
      name = re.compile(r'^(title|name):\s*', re.IGNORECASE).sub('', name).strip()
      return NoteItem(name=name, body=data)
    if contentType == constants.TYPE_SIF_NOTE:
      data = ET.parse(stream).getroot()
      ret = NoteItem(name=data.findtext('Subject'), body=data.findtext('Body'))
      for child in data:
        if child.tag in ('SIFVersion', 'Subject', 'Body'):
          continue
        ret.addExtension(child.tag, child.text)
      return ret
    raise common.InvalidContentType('cannot de-serialize NoteItem from "%s"' % (contentType,))