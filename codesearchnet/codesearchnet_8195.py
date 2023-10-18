def dumps(data, use_yaml=None, safe=True, **kwds):
    """
    Dumps data into a nicely formatted JSON string.

    :param dict data: a dictionary to dump
    :param kwds: keywords to pass to json.dumps
    :returns: a string with formatted data
    :rtype: str
    """
    if use_yaml is None:
        use_yaml = ALWAYS_DUMP_YAML

    if use_yaml:
        dumps = yaml.safe_dump if safe else yaml.dump
    else:
        dumps = json.dumps
        kwds.update(indent=4, sort_keys=True)
        if not safe:
            kwds.update(default=repr)
    return dumps(data, **kwds)