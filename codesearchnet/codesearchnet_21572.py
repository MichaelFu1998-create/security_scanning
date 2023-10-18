def get_lsst_bibtex(bibtex_filenames=None):
    """Get content of lsst-texmf bibliographies.

    BibTeX content is downloaded from GitHub (``master`` branch of
    https://github.com/lsst/lsst-texmf or retrieved from an in-memory cache.

    Parameters
    ----------
    bibtex_filenames : sequence of `str`, optional
        List of lsst-texmf BibTeX files to retrieve. These can be the filenames
        of lsst-bibtex files (for example, ``['lsst.bib', 'lsst-dm.bib']``)
        or names without an extension (``['lsst', 'lsst-dm']``). The default
        (recommended) is to get *all* lsst-texmf bibliographies:

        .. code-block:: python

           ['lsst', 'lsst-dm', 'refs', 'books', 'refs_ads']

    Returns
    -------
    bibtex : `dict`
        Dictionary with keys that are bibtex file names (such as ``'lsst'``,
        ``'lsst-dm'``). Values are the corresponding bibtex file content
        (`str`).
    """
    logger = logging.getLogger(__name__)

    if bibtex_filenames is None:
        # Default lsst-texmf bibliography files
        bibtex_names = KNOWN_LSSTTEXMF_BIB_NAMES
    else:
        # Sanitize filenames (remove extensions, path)
        bibtex_names = []
        for filename in bibtex_filenames:
            name = os.path.basename(os.path.splitext(filename)[0])
            if name not in KNOWN_LSSTTEXMF_BIB_NAMES:
                logger.warning('%r is not a known lsst-texmf bib file',
                               name)
                continue
            bibtex_names.append(name)

    # names of bibtex files not in cache
    uncached_names = [name for name in bibtex_names
                      if name not in _LSSTTEXMF_BIB_CACHE]
    if len(uncached_names) > 0:
        # Download bibtex and put into the cache
        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(_download_lsst_bibtex(uncached_names))
        loop.run_until_complete(future)
        for name, text in zip(bibtex_names, future.result()):
            _LSSTTEXMF_BIB_CACHE[name] = text

    return {name: _LSSTTEXMF_BIB_CACHE[name] for name in bibtex_names}