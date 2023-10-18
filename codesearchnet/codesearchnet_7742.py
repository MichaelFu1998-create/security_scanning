def init(path):
    """Copy a sample config file in the current directory (default to
    'sigal.conf.py'), or use the provided 'path'."""

    if os.path.isfile(path):
        print("Found an existing config file, will abort to keep it safe.")
        sys.exit(1)

    from pkg_resources import resource_string
    conf = resource_string(__name__, 'templates/sigal.conf.py')

    with open(path, 'w', encoding='utf-8') as f:
        f.write(conf.decode('utf8'))
    print("Sample config file created: {}".format(path))