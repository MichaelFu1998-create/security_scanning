def cached_download(url, name):

    """Download the data at a URL, and cache it under the given name.

    The file is stored under `pyav/test` with the given name in the directory
    :envvar:`PYAV_TESTDATA_DIR`, or the first that is writeable of:

    - the current virtualenv
    - ``/usr/local/share``
    - ``/usr/local/lib``
    - ``/usr/share``
    - ``/usr/lib``
    - the user's home

    """

    clean_name = os.path.normpath(name)
    if clean_name != name:
        raise ValueError("{} is not normalized.".format(name))

    for dir_ in iter_data_dirs():
        path = os.path.join(dir_, name)
        if os.path.exists(path):
            return path

    dir_ = next(iter_data_dirs(True))
    path = os.path.join(dir_, name)

    log.info("Downloading {} to {}".format(url, path))

    response = urlopen(url)
    if response.getcode() != 200:
        raise ValueError("HTTP {}".format(response.getcode()))

    dir_ = os.path.dirname(path)
    try:
        os.makedirs(dir_)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    tmp_path = path + '.tmp'
    with open(tmp_path, 'wb') as fh:
        while True:
            chunk = response.read(8196)
            if chunk:
                fh.write(chunk)
            else:
                break

    os.rename(tmp_path, path)

    return path