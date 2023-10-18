def trans_new(name, transform, inverse, breaks=None,
              minor_breaks=None, _format=None,
              domain=(-np.inf, np.inf), doc='', **kwargs):
    """
    Create a transformation class object

    Parameters
    ----------
    name : str
        Name of the transformation
    transform : callable ``f(x)``
        A function (preferably a `ufunc`) that computes
        the transformation.
    inverse : callable ``f(x)``
        A function (preferably a `ufunc`) that computes
        the inverse of the transformation.
    breaks : callable ``f(limits)``
        Function to compute the breaks for this transform.
        If None, then a default good enough for a linear
        domain is used.
    minor_breaks : callable ``f(major, limits)``
        Function to compute the minor breaks for this
        transform. If None, then a default good enough for
        a linear domain is used.
    _format : callable ``f(breaks)``
        Function to format the generated breaks.
    domain : array_like
        Domain over which the transformation is valid.
        It should be of length 2.
    doc : str
        Docstring for the class.
    **kwargs : dict
        Attributes of the transform, e.g if base is passed
        in kwargs, then `t.base` would be a valied attribute.

    Returns
    -------
    out : trans
        Transform class
    """
    def _get(func):
        if isinstance(func, (classmethod, staticmethod, MethodType)):
            return func
        else:
            return staticmethod(func)

    klass_name = '{}_trans'.format(name)

    d = {'transform': _get(transform),
         'inverse': _get(inverse),
         'domain': domain,
         '__doc__': doc,
         **kwargs}

    if breaks:
        d['breaks_'] = _get(breaks)

    if minor_breaks:
        d['minor_breaks'] = _get(minor_breaks)

    if _format:
        d['format'] = _get(_format)

    return type(klass_name, (trans,), d)