def get_library_config(name):
    """Get distutils-compatible extension extras for the given library.

    This requires ``pkg-config``.

    """
    try:
        proc = Popen(['pkg-config', '--cflags', '--libs', name], stdout=PIPE, stderr=PIPE)
    except OSError:
        print('pkg-config is required for building PyAV')
        exit(1)

    raw_cflags, err = proc.communicate()
    if proc.wait():
        return

    known, unknown = parse_cflags(raw_cflags.decode('utf8'))
    if unknown:
        print("pkg-config returned flags we don't understand: {}".format(unknown))
        exit(1)

    return known