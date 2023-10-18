def loadsItem(self, data, contentType=None, version=None):
    '''
    [OPTIONAL] Identical to :meth:`loadItem`, except the serialized
    form is provided as a string representation in `data` instead of
    as a stream. The default implementation just wraps
    :meth:`loadItem`.
    '''
    buf = six.StringIO(data)
    return self.loadItem(buf, contentType, version)