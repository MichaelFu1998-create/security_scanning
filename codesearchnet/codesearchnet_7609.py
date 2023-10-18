def parse_sphinx_searchindex(searchindex):
    """Parse a Sphinx search index

    Parameters
    ----------
    searchindex : str
        The Sphinx search index (contents of searchindex.js)

    Returns
    -------
    filenames : list of str
        The file names parsed from the search index.
    objects : dict
        The objects parsed from the search index.
    """
    # Make sure searchindex uses UTF-8 encoding
    if hasattr(searchindex, 'decode'):
        searchindex = searchindex.decode('UTF-8')

    # parse objects
    query = 'objects:'
    pos = searchindex.find(query)
    if pos < 0:
        raise ValueError('"objects:" not found in search index')

    sel = _select_block(searchindex[pos:], '{', '}')
    objects = _parse_dict_recursive(sel)

    # parse filenames
    query = 'filenames:'
    pos = searchindex.find(query)
    if pos < 0:
        raise ValueError('"filenames:" not found in search index')
    filenames = searchindex[pos + len(query) + 1:]
    filenames = filenames[:filenames.find(']')]
    filenames = [f.strip('"') for f in filenames.split(',')]

    return filenames, objects