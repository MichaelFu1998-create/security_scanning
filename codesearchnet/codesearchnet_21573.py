def get_bibliography(lsst_bib_names=None, bibtex=None):
    """Make a pybtex BibliographyData instance from standard lsst-texmf
    bibliography files and user-supplied bibtex content.

    Parameters
    ----------
    lsst_bib_names : sequence of `str`, optional
        Names of lsst-texmf BibTeX files to include. For example:

        .. code-block:: python

           ['lsst', 'lsst-dm', 'refs', 'books', 'refs_ads']

        Default is `None`, which includes all lsst-texmf bibtex files.

    bibtex : `str`
        BibTeX source content not included in lsst-texmf. This can be content
        from a import ``local.bib`` file.

    Returns
    -------
    bibliography : `pybtex.database.BibliographyData`
        A pybtex bibliography database that includes all given sources:
        lsst-texmf bibliographies and ``bibtex``.
    """
    bibtex_data = get_lsst_bibtex(bibtex_filenames=lsst_bib_names)

    # Parse with pybtex into BibliographyData instances
    pybtex_data = [pybtex.database.parse_string(_bibtex, 'bibtex')
                   for _bibtex in bibtex_data.values()]

    # Also parse local bibtex content
    if bibtex is not None:
        pybtex_data.append(pybtex.database.parse_string(bibtex, 'bibtex'))

    # Merge BibliographyData
    bib = pybtex_data[0]
    if len(pybtex_data) > 1:
        for other_bib in pybtex_data[1:]:
            for key, entry in other_bib.entries.items():
                bib.add_entry(key, entry)

    return bib