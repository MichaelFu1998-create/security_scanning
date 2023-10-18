def xmatch_cpdir_external_catalogs(cpdir,
                                   xmatchpkl,
                                   cpfileglob='checkplot-*.pkl*',
                                   xmatchradiusarcsec=2.0,
                                   updateexisting=True,
                                   resultstodir=None):
    '''This xmatches external catalogs to all checkplots in a directory.

    Parameters
    -----------

    cpdir : str
        This is the directory to search in for checkplots.

    xmatchpkl : str
        The filename of a pickle prepared beforehand with the
        `checkplot.pkl_xmatch.load_xmatch_external_catalogs` function,
        containing collected external catalogs to cross-match the objects in the
        input `cplist` against.

    cpfileglob : str
        This is the UNIX fileglob to use in searching for checkplots.

    xmatchradiusarcsec : float
        The match radius to use for the cross-match in arcseconds.

    updateexisting : bool
        If this is True, will only update the `xmatch` dict in each checkplot
        pickle with any new cross-matches to the external catalogs. If False,
        will overwrite the `xmatch` dict with results from the current run.

    resultstodir : str or None
        If this is provided, then it must be a directory to write the resulting
        checkplots to after xmatch is done. This can be used to keep the
        original checkplots in pristine condition for some reason.

    Returns
    -------

    dict
        Returns a dict with keys = input checkplot pickle filenames and vals =
        xmatch status dict for each checkplot pickle.

    '''

    cplist = glob.glob(os.path.join(cpdir, cpfileglob))

    return xmatch_cplist_external_catalogs(
        cplist,
        xmatchpkl,
        xmatchradiusarcsec=xmatchradiusarcsec,
        updateexisting=updateexisting,
        resultstodir=resultstodir
    )