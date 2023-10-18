def _tup_and_byte(obj):
    """ wat """
    # if this is a unicode string, return its string representation
    if isinstance(obj, unicode):
        return obj.encode('utf-8')

    # if this is a list of values, return list of byteified values
    if isinstance(obj, list):
        return [_tup_and_byte(item) for item in obj]

    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(obj, dict):
        if "__tuple__" in obj:
            return tuple(_tup_and_byte(item) for item in obj["items"])
        else:
            return {
                _tup_and_byte(key): _tup_and_byte(val) for \
                key, val in obj.iteritems()
        }

    # if it's anything else, return it in its original form
    return obj