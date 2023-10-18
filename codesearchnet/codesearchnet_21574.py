def get_url_from_entry(entry):
    """Get a usable URL from a pybtex entry.

    Parameters
    ----------
    entry : `pybtex.database.Entry`
        A pybtex bibliography entry.

    Returns
    -------
    url : `str`
        Best available URL from the ``entry``.

    Raises
    ------
    NoEntryUrlError
        Raised when no URL can be made from the bibliography entry.

    Notes
    -----
    The order of priority is:

    1. ``url`` field
    2. ``ls.st`` URL from the handle for ``@docushare`` entries.
    3. ``adsurl``
    4. DOI
    """
    if 'url' in entry.fields:
        return entry.fields['url']
    elif entry.type.lower() == 'docushare':
        return 'https://ls.st/' + entry.fields['handle']
    elif 'adsurl' in entry.fields:
        return entry.fields['adsurl']
    elif 'doi' in entry.fields:
        return 'https://doi.org/' + entry.fields['doi']
    else:
        raise NoEntryUrlError()