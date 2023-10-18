def _byteify(data, ignore_dicts=False):
    """
    converts unicode to utf-8 when reading in json files
    """
    if isinstance(data, unicode):
        return data.encode("utf-8")

    if isinstance(data, list):
        return [_byteify(item, ignore_dicts=True) for item in data]

    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    return data