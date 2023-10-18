async def _download_lsst_bibtex(bibtex_names):
    """Asynchronously download a set of lsst-texmf BibTeX bibliographies from
    GitHub.

    Parameters
    ----------
    bibtex_names : sequence of `str`
        Names of lsst-texmf BibTeX files to download. For example:

        .. code-block:: python

           ['lsst', 'lsst-dm', 'refs', 'books', 'refs_ads']

    Returns
    -------
    bibtexs : `list` of `str`
        List of BibTeX file content, in the same order as ``bibtex_names``.
    """
    blob_url_template = (
        'https://raw.githubusercontent.com/lsst/lsst-texmf/master/texmf/'
        'bibtex/bib/{name}.bib'
    )
    urls = [blob_url_template.format(name=name) for name in bibtex_names]

    tasks = []
    async with ClientSession() as session:
        for url in urls:
            task = asyncio.ensure_future(_download_text(url, session))
            tasks.append(task)

        return await asyncio.gather(*tasks)