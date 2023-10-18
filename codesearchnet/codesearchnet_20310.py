def _pattern(*names, **kwargs):
    """Returns globbing pattern for name1/name2/../lastname + '--*' or
    name1/name2/../lastname + extension if parameter `extension` it set.

    Parameters
    ----------
    names : strings
        Which path to join. Example: _pattern('path', 'to', 'experiment') will
        return `path/to/experiment--*`.
    extension : string
        If other extension then --* is wanted.
        Example: _pattern('path', 'to', 'image', extension='*.png') will return
        `path/to/image*.png`.

    Returns
    -------
    string
        Joined glob pattern string.
    """
    if 'extension' not in kwargs:
        kwargs['extension'] = '--*'
    return os.path.join(*names) + kwargs['extension']