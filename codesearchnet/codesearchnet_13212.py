def can_convert(annotation, target_namespace):
    '''Test if an annotation can be mapped to a target namespace

    Parameters
    ----------
    annotation : jams.Annotation
        An annotation object

    target_namespace : str
        The target namespace

    Returns
    -------
    True
        if `annotation` can be automatically converted to
        `target_namespace`

    False
        otherwise
    '''

    # If we're already in the target namespace, do nothing
    if annotation.namespace == target_namespace:
        return True

    if target_namespace in __CONVERSION__:
        # Look for a way to map this namespace to the target
        for source in __CONVERSION__[target_namespace]:
            if annotation.search(namespace=source):
                return True
    return False