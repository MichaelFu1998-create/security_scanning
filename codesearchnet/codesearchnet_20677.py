def is_img(obj):
    """ Check for get_data and get_affine method in an object

    Parameters
    ----------
    obj: any object
        Tested object

    Returns
    -------
    is_img: boolean
        True if get_data and get_affine methods are present and callable,
        False otherwise.
    """
    try:
        get_data   = getattr(obj, 'get_data')
        get_affine = getattr(obj, 'get_affine')

        return isinstance(get_data,   collections.Callable) and \
               isinstance(get_affine, collections.Callable)
    except AttributeError:
        return False