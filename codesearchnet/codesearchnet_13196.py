def namespace_array(ns_key):
    '''Construct a validation schema for arrays of a given namespace.

    Parameters
    ----------
    ns_key : str
        Namespace key identifier

    Returns
    -------
    schema : dict
        JSON schema of `namespace` observation arrays
    '''

    obs_sch = namespace(ns_key)
    obs_sch['title'] = 'Observation'

    sch = copy.deepcopy(JAMS_SCHEMA['definitions']['SparseObservationList'])
    sch['items'] = obs_sch
    return sch