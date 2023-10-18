def expand_filepaths(base_dir, rel_paths):
    """Expand a list of relative paths to a give base directory.

    Parameters
    ----------
    base_dir : str
        The target base directory

    rel_paths : list (or list-like)
        Collection of relative path strings

    Returns
    -------
    expanded_paths : list
        `rel_paths` rooted at `base_dir`

    Examples
    --------
    >>> jams.util.expand_filepaths('/data', ['audio', 'beat', 'seglab'])
    ['/data/audio', '/data/beat', '/data/seglab']

    """
    return [os.path.join(base_dir, os.path.normpath(rp)) for rp in rel_paths]