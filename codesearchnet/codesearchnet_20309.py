def attributes(path):
    """Get attributes from path based on format --[A-Z]. Returns namedtuple
    with upper case attributes equal to what found in path (string) and lower
    case as int. If path holds several occurrences of same character, only the
    last one is kept.

        >>> attrs = attributes('/folder/file--X00-X01.tif')
        >>> print(attrs)
        namedtuple('attributes', 'X x')('01', 1)
        >>> print(attrs.x)
        1

    Parameters
    ----------
    path : string

    Returns
    -------
    collections.namedtuple
    """
    # number of charcters set to numbers have changed in LAS AF X !!
    matches = re.findall('--([A-Z]{1})([0-9]{2,4})', path)

    keys = []
    values = []
    for k,v in matches:
        if k in keys:
            # keep only last key
            i = keys.index(k)
            del keys[i]
            del values[i]
        keys.append(k)
        values.append(v)

    lower_keys = [k.lower() for k in keys]
    int_values= [int(v) for v in values]

    attributes = namedtuple('attributes', keys + lower_keys)

    return attributes(*values + int_values)