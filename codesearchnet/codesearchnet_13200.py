def __get_dtype(typespec):
    '''Get the dtype associated with a jsonschema type definition

    Parameters
    ----------
    typespec : dict
        The schema definition

    Returns
    -------
    dtype : numpy.dtype
        The associated dtype
    '''

    if 'type' in typespec:
        return __TYPE_MAP__.get(typespec['type'], np.object_)

    elif 'enum' in typespec:
        # Enums map to objects
        return np.object_

    elif 'oneOf' in typespec:
        # Recurse
        types = [__get_dtype(v) for v in typespec['oneOf']]

        # If they're not all equal, return object
        if all([t == types[0] for t in types]):
            return types[0]

    return np.object_