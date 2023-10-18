def xmatch_cplist_external_catalogs(cplist,
                                    xmatchpkl,
                                    xmatchradiusarcsec=2.0,
                                    updateexisting=True,
                                    resultstodir=None):
    '''This xmatches external catalogs to a collection of checkplots.

    Parameters
    ----------

    cplist : list of str
        This is the list of checkplot pickle files to process.

    xmatchpkl : str
        The filename of a pickle prepared beforehand with the
        `checkplot.pkl_xmatch.load_xmatch_external_catalogs` function,
        containing collected external catalogs to cross-match the objects in the
        input `cplist` against.

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

    # load the external catalog
    with open(xmatchpkl,'rb') as infd:
        xmd = pickle.load(infd)

    # match each object. this is fairly fast, so this is not parallelized at the
    # moment

    status_dict = {}

    for cpf in cplist:

        cpd = _read_checkplot_picklefile(cpf)

        try:

            # match in place
            xmatch_external_catalogs(cpd, xmd,
                                     xmatchradiusarcsec=xmatchradiusarcsec,
                                     updatexmatch=updateexisting)

            for xmi in cpd['xmatch']:

                if cpd['xmatch'][xmi]['found']:
                    LOGINFO('checkplot %s: %s matched to %s, '
                            'match dist: %s arcsec' %
                            (os.path.basename(cpf),
                             cpd['objectid'],
                             cpd['xmatch'][xmi]['name'],
                             cpd['xmatch'][xmi]['distarcsec']))

                if not resultstodir:
                    outcpf = _write_checkplot_picklefile(cpd,
                                                         outfile=cpf)
                else:
                    xcpf = os.path.join(resultstodir, os.path.basename(cpf))
                    outcpf = _write_checkplot_picklefile(cpd,
                                                         outfile=xcpf)

            status_dict[cpf] = outcpf

        except Exception as e:

            LOGEXCEPTION('failed to match objects for %s' % cpf)
            status_dict[cpf] = None

    return status_dict