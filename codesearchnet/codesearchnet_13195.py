def namespace(ns_key):
    '''Construct a validation schema for a given namespace.

    Parameters
    ----------
    ns_key : str
        Namespace key identifier (eg, 'beat' or 'segment_tut')

    Returns
    -------
    schema : dict
        JSON schema of `namespace`
    '''

    if ns_key not in __NAMESPACE__:
        raise NamespaceError('Unknown namespace: {:s}'.format(ns_key))

    sch = copy.deepcopy(JAMS_SCHEMA['definitions']['SparseObservation'])

    for key in ['value', 'confidence']:
        try:
            sch['properties'][key] = __NAMESPACE__[ns_key][key]
        except KeyError:
            pass

    return sch