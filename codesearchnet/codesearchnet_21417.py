def toSyncML(self, nodeName=None, uniqueVerCt=False):
    '''
    Returns an ElementTree node representing this ContentTypeInfo. If
    `nodeName` is not None, then it will be used as the containing
    element node name (this is useful, for example, to differentiate
    between a standard content-type and a preferred content-type). If
    `uniqueVerCt` is True, then an array of elements will be returned
    instead of a single element with multiple VerCT elements (for
    content-types that support multiple versions).
    '''
    if uniqueVerCt:
      ret = []
      for v in self.versions:
        tmp = ET.Element(nodeName or 'ContentType')
        ET.SubElement(tmp, 'CTType').text = self.ctype
        ET.SubElement(tmp, 'VerCT').text = v
        ret.append(tmp)
      return ret
    ret = ET.Element(nodeName or 'ContentType')
    ET.SubElement(ret, 'CTType').text = self.ctype
    for v in self.versions:
      ET.SubElement(ret, 'VerCT').text = v
    return ret