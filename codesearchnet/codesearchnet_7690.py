def _data_root_Linux():
    """
    Use freedesktop.org Base Dir Specfication to determine storage
    location.
    """
    fallback = os.path.expanduser('~/.local/share')
    root = os.environ.get('XDG_DATA_HOME', None) or fallback
    return os.path.join(root, 'python_keyring')