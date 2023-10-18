def flatten_dtype(dtype, _next=None):
    """ Unpack a structured data-type.  """
    types = []
    if _next is None: 
        _next = [0, '']
        primary = True
    else:
        primary = False

    prefix = _next[1]

    if dtype.names is None:
        for i in numpy.ndindex(dtype.shape):
            if dtype.base == dtype:
                types.append(('%s%s' % (prefix, simplerepr(i)), dtype))
                _next[0] += 1
            else:
                _next[1] = '%s%s' % (prefix, simplerepr(i))
                types.extend(flatten_dtype(dtype.base, _next))
    else:
        for field in dtype.names:
            typ_fields = dtype.fields[field]
            if len(prefix) > 0:
                _next[1] = prefix + '.' + field
            else:
                _next[1] = '' + field
            flat_dt = flatten_dtype(typ_fields[0], _next)
            types.extend(flat_dt)

    _next[1] = prefix
    if primary:
        return numpy.dtype(types)
    else:
        return types