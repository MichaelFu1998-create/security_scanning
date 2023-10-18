def get_varfeatures(simbasedir,
                    mindet=1000,
                    nworkers=None):
    '''This runs `lcproc.lcvfeatures.parallel_varfeatures` on fake LCs in
    `simbasedir`.

    Parameters
    ----------

    simbasedir : str
        The directory containing the fake LCs to process.

    mindet : int
        The minimum number of detections needed to accept an LC and process it.

    nworkers : int or None
        The number of parallel workers to use when extracting variability
        features from the input light curves.

    Returns
    -------

    str
        The path to the `varfeatures` pickle created after running the
        `lcproc.lcvfeatures.parallel_varfeatures` function.

    '''

    # get the info from the simbasedir
    with open(os.path.join(simbasedir, 'fakelcs-info.pkl'),'rb') as infd:
        siminfo = pickle.load(infd)

    lcfpaths = siminfo['lcfpath']
    varfeaturedir = os.path.join(simbasedir,'varfeatures')

    # get the column defs for the fakelcs
    timecols = siminfo['timecols']
    magcols = siminfo['magcols']
    errcols = siminfo['errcols']

    # get the column defs for the fakelcs
    timecols = siminfo['timecols']
    magcols = siminfo['magcols']
    errcols = siminfo['errcols']

    # register the fakelc pklc as a custom lcproc format
    # now we should be able to use all lcproc functions correctly
    fakelc_formatkey = 'fake-%s' % siminfo['lcformat']
    lcproc.register_lcformat(
        fakelc_formatkey,
        '*-fakelc.pkl',
        timecols,
        magcols,
        errcols,
        'astrobase.lcproc',
        '_read_pklc',
        magsarefluxes=siminfo['magsarefluxes']
    )

    # now we can use lcproc.parallel_varfeatures directly
    varinfo = lcvfeatures.parallel_varfeatures(lcfpaths,
                                               varfeaturedir,
                                               lcformat=fakelc_formatkey,
                                               mindet=mindet,
                                               nworkers=nworkers)

    with open(os.path.join(simbasedir,'fakelc-varfeatures.pkl'),'wb') as outfd:
        pickle.dump(varinfo, outfd, pickle.HIGHEST_PROTOCOL)

    return os.path.join(simbasedir,'fakelc-varfeatures.pkl')