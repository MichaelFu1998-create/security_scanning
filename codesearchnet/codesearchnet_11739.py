def oct(v, **kwargs): # pylint: disable=redefined-builtin
    """
    A backwards compatible version of oct() that works with Python2.7 and Python3.
    """
    v = str(v)
    if six.PY2:
        if v.startswith('0o'):
            v = '0' + v[2:]
    else:
        if not v.starswith('0o'):
            assert v[0] == '0'
            v = '0o' + v[1:]
    return eval('_oct(%s, **kwargs)' % v)