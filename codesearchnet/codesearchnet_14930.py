def molconvert_chemaxon(data):
    """
    molconvert wrapper
    :param data: buffer or string or path to file
    :return: array of molecules of reactions
    """
    if isinstance(data, Path):
        with data.open('rb') as f:
            data = f.read()
    elif isinstance(data, StringIO):
        data = data.read().encode()
    elif isinstance(data, BytesIO):
        data = data.read()
    elif hasattr(data, 'read'):  # check if data is open(filename, mode)
        data = data.read()
        if isinstance(data, str):
            data = data.encode()
    elif isinstance(data, str):
        data = data.encode()
    elif not isinstance(data, bytes):
        raise ValueError('invalid input')

    try:
        p = run(['molconvert', '-g', 'mrv'], input=data, stdout=PIPE)
    except FileNotFoundError as e:
        raise ConfigurationError from e

    if p.returncode != 0:
        raise ConfigurationError(p.stderr.decode())

    with BytesIO(p.stdout) as f, MRVread(f) as r:
        return iter2array(r)