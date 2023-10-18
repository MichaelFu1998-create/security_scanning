def PushPopItem(obj, key, value):
    '''
    A context manager to replace and restore a value using a getter and setter.

    :param object obj: The object to replace/restore.
    :param object key: The key to replace/restore in the object.
    :param object value: The value to replace.

    Example::

      with PushPop2(sys.modules, 'alpha', None):
        pytest.raises(ImportError):
          import alpha
    '''
    if key in obj:
        old_value = obj[key]
        obj[key] = value
        yield value
        obj[key] = old_value

    else:
        obj[key] = value
        yield value
        del obj[key]