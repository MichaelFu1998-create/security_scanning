def disable():
    """
    Configure the null keyring as the default.
    """
    root = platform.config_root()
    try:
        os.makedirs(root)
    except OSError:
        pass
    filename = os.path.join(root, 'keyringrc.cfg')
    if os.path.exists(filename):
        msg = "Refusing to overwrite {filename}".format(**locals())
        raise RuntimeError(msg)
    with open(filename, 'w') as file:
        file.write('[backend]\ndefault-keyring=keyring.backends.null.Keyring')