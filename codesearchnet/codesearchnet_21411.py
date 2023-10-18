def dumps(self, contentType=None, version=None):
    '''
    [OPTIONAL] Identical to :meth:`dump`, except the serialized form
    is returned as a string representation. As documented in
    :meth:`dump`, the return value can optionally be a three-element
    tuple of (contentType, version, data) if the provided content-type
    should be overridden or enhanced. The default implementation just
    wraps :meth:`dump`.
    '''
    buf = six.StringIO()
    ret = self.dump(buf, contentType, version)
    if ret is None:
      return buf.getvalue()
    return (ret[0], ret[1], buf.getvalue())