def loads(cls, data, contentType=None, version=None):
    '''
    [OPTIONAL] Identical to :meth:`load`, except the serialized form
    is provided as a string representation in `data` instead of as a
    stream. The default implementation just wraps :meth:`load`.
    '''
    buf = six.StringIO(data)
    return cls.load(buf, contentType, version)