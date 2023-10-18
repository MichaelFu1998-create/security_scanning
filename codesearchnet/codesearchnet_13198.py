def get_dtypes(ns_key):
    '''Get the dtypes associated with the value and confidence fields
    for a given namespace.

    Parameters
    ----------
    ns_key : str
        The namespace key in question

    Returns
    -------
    value_dtype, confidence_dtype : numpy.dtype
        Type identifiers for value and confidence fields.
    '''

    # First, get the schema
    if ns_key not in __NAMESPACE__:
        raise NamespaceError('Unknown namespace: {:s}'.format(ns_key))

    value_dtype = __get_dtype(__NAMESPACE__[ns_key].get('value', {}))
    confidence_dtype = __get_dtype(__NAMESPACE__[ns_key].get('confidence', {}))

    return value_dtype, confidence_dtype