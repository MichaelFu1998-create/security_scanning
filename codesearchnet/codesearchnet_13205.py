def find_with_extension(in_dir, ext, depth=3, sort=True):
    """Naive depth-search into a directory for files with a given extension.

    Parameters
    ----------
    in_dir : str
        Path to search.
    ext : str
        File extension to match.
    depth : int
        Depth of directories to search.
    sort : bool
        Sort the list alphabetically

    Returns
    -------
    matched : list
        Collection of matching file paths.

    Examples
    --------
    >>> jams.util.find_with_extension('Audio', 'wav')
    ['Audio/LizNelson_Rainfall/LizNelson_Rainfall_MIX.wav',
     'Audio/LizNelson_Rainfall/LizNelson_Rainfall_RAW/LizNelson_Rainfall_RAW_01_01.wav',
     'Audio/LizNelson_Rainfall/LizNelson_Rainfall_RAW/LizNelson_Rainfall_RAW_02_01.wav',
     ...
     'Audio/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_02.wav',
     'Audio/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_03.wav',
    'Audio/Phoenix_ScotchMorris/Phoenix_ScotchMorris_STEMS/Phoenix_ScotchMorris_STEM_04.wav']

    """
    assert depth >= 1
    ext = ext.strip(os.extsep)
    match = list()
    for n in range(1, depth+1):
        wildcard = os.path.sep.join(["*"]*n)
        search_path = os.path.join(in_dir, os.extsep.join([wildcard, ext]))
        match += glob.glob(search_path)

    if sort:
        match.sort()
    return match