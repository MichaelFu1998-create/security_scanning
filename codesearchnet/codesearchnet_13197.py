def values(ns_key):
    '''Return the allowed values for an enumerated namespace.

    Parameters
    ----------
    ns_key : str
        Namespace key identifier

    Returns
    -------
    values : list

    Raises
    ------
    NamespaceError
        If `ns_key` is not found, or does not have enumerated values

    Examples
    --------
    >>> jams.schema.values('tag_gtzan')
    ['blues', 'classical', 'country', 'disco', 'hip-hop', 'jazz',
     'metal', 'pop', 'reggae', 'rock']
    '''

    if ns_key not in __NAMESPACE__:
        raise NamespaceError('Unknown namespace: {:s}'.format(ns_key))

    if 'enum' not in __NAMESPACE__[ns_key]['value']:
        raise NamespaceError('Namespace {:s} is not enumerated'.format(ns_key))

    return copy.copy(__NAMESPACE__[ns_key]['value']['enum'])