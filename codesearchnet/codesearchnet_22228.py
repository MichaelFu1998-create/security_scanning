def get_obj_attr(obj, attr):
    """Works like getattr() but supports django's double underscore object
    dereference notation.

    Example usage:

    .. code-block:: python

        >>> get_obj_attr(book, 'writer__age')
        42
        >>> get_obj_attr(book, 'publisher__address')
        <Address object at 105a79ac8>

    :param obj: 
        Object to start the derference from

    :param attr:
        String name of attribute to return

    :returns:
        Derferenced object 

    :raises:
        AttributeError in the attribute in question does not exist
    """
    # handle '__' referencing like in QuerySets
    fields = attr.split('__')
    field_obj = getattr(obj, fields[0])

    for field in fields[1:]:
        # keep going down the reference tree
        field_obj = getattr(field_obj, field)

    return field_obj