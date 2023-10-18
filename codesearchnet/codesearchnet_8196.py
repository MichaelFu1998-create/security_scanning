def dump(data, file=sys.stdout, use_yaml=None, **kwds):
    """
    Dumps data as nicely formatted JSON string to a file or file handle

    :param dict data: a dictionary to dump
    :param file: a filename or file handle to write to
    :param kwds: keywords to pass to json.dump
    """
    if use_yaml is None:
        use_yaml = ALWAYS_DUMP_YAML

    def dump(fp):
        if use_yaml:
            yaml.safe_dump(data, stream=fp, **kwds)
        else:
            json.dump(data, fp, indent=4, sort_keys=True, **kwds)

    if not isinstance(file, str):
        return dump(file)

    if os.path.isabs(file):
        parent = os.path.dirname(file)
        if not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)

    with open(file, 'w') as fp:
        return dump(fp)