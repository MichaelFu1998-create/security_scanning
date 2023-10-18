def parallel_periodicfeatures(pfpkl_list,
                              lcbasedir,
                              outdir,
                              starfeaturesdir=None,
                              fourierorder=5,
                              # these are depth, duration, ingress duration
                              transitparams=(-0.01,0.1,0.1),
                              # these are depth, duration, depth ratio, secphase
                              ebparams=(-0.2,0.3,0.7,0.5),
                              pdiff_threshold=1.0e-4,
                              sidereal_threshold=1.0e-4,
                              sampling_peak_multiplier=5.0,
                              sampling_startp=None,
                              sampling_endp=None,
                              timecols=None,
                              magcols=None,
                              errcols=None,
                              lcformat='hat-sql',
                              lcformatdir=None,
                              sigclip=10.0,
                              verbose=False,
                              maxobjects=None,
                              nworkers=NCPUS):
    '''This runs periodic feature generation in parallel for all periodfinding
    pickles in the input list.

    Parameters
    ----------

    pfpkl_list : list of str
        The list of period-finding pickles to use.

    lcbasedir : str
        The base directory where the associated light curves are located.

    outdir : str
        The directory where the results will be written.

    starfeaturesdir : str or None
        The directory containing the `starfeatures-<objectid>.pkl` files for
        each object to use calculate neighbor proximity light curve features.

    fourierorder : int
        The Fourier order to use to generate sinusoidal function and fit that to
        the phased light curve.

    transitparams : list of floats
        The transit depth, duration, and ingress duration to use to generate a
        trapezoid planet transit model fit to the phased light curve. The period
        used is the one provided in `period`, while the epoch is automatically
        obtained from a spline fit to the phased light curve.

    ebparams : list of floats
        The primary eclipse depth, eclipse duration, the primary-secondary depth
        ratio, and the phase of the secondary eclipse to use to generate an
        eclipsing binary model fit to the phased light curve. The period used is
        the one provided in `period`, while the epoch is automatically obtained
        from a spline fit to the phased light curve.

    pdiff_threshold : float
        This is the max difference between periods to consider them the same.

    sidereal_threshold : float
        This is the max difference between any of the 'best' periods and the
        sidereal day periods to consider them the same.

    sampling_peak_multiplier : float
        This is the minimum multiplicative factor of a 'best' period's
        normalized periodogram peak over the sampling periodogram peak at the
        same period required to accept the 'best' period as possibly real.

    sampling_startp, sampling_endp : float
        If the `pgramlist` doesn't have a time-sampling Lomb-Scargle
        periodogram, it will be obtained automatically. Use these kwargs to
        control the minimum and maximum period interval to be searched when
        generating this periodogram.

    timecols : list of str or None
        The timecol keys to use from the lcdict in calculating the features.

    magcols : list of str or None
        The magcol keys to use from the lcdict in calculating the features.

    errcols : list of str or None
        The errcol keys to use from the lcdict in calculating the features.

    lcformat : str
        This is the `formatkey` associated with your light curve format, which
        you previously passed in to the `lcproc.register_lcformat`
        function. This will be used to look up how to find and read the light
        curves specified in `basedir` or `use_list_of_filenames`.

    lcformatdir : str or None
        If this is provided, gives the path to a directory when you've stored
        your lcformat description JSONs, other than the usual directories lcproc
        knows to search for them in. Use this along with `lcformat` to specify
        an LC format JSON file that's not currently registered with lcproc.

    sigclip : float or int or sequence of two floats/ints or None
        If a single float or int, a symmetric sigma-clip will be performed using
        the number provided as the sigma-multiplier to cut out from the input
        time-series.

        If a list of two ints/floats is provided, the function will perform an
        'asymmetric' sigma-clip. The first element in this list is the sigma
        value to use for fainter flux/mag values; the second element in this
        list is the sigma value to use for brighter flux/mag values. For
        example, `sigclip=[10., 3.]`, will sigclip out greater than 10-sigma
        dimmings and greater than 3-sigma brightenings. Here the meaning of
        "dimming" and "brightening" is set by *physics* (not the magnitude
        system), which is why the `magsarefluxes` kwarg must be correctly set.

        If `sigclip` is None, no sigma-clipping will be performed, and the
        time-series (with non-finite elems removed) will be passed through to
        the output.

    verbose : bool
        If True, will indicate progress while working.

    maxobjects : int
        The total number of objects to process from `pfpkl_list`.

    nworkers : int
        The number of parallel workers to launch to process the input.

    Returns
    -------

    dict
        A dict containing key: val pairs of the input period-finder result and
        the output periodic feature result pickles for each input pickle is
        returned.

    '''
    # make sure to make the output directory if it doesn't exist
    if not os.path.exists(outdir):
        os.makedirs(outdir)

    if maxobjects:
        pfpkl_list = pfpkl_list[:maxobjects]

    LOGINFO('%s periodfinding pickles to process' % len(pfpkl_list))

    # if the starfeaturedir is provided, try to find a starfeatures pickle for
    # each periodfinding pickle in pfpkl_list
    if starfeaturesdir and os.path.exists(starfeaturesdir):

        starfeatures_list = []

        LOGINFO('collecting starfeatures pickles...')

        for pfpkl in pfpkl_list:

            sfpkl1 = os.path.basename(pfpkl).replace('periodfinding',
                                                     'starfeatures')
            sfpkl2 = sfpkl1.replace('.gz','')

            sfpath1 = os.path.join(starfeaturesdir, sfpkl1)
            sfpath2 = os.path.join(starfeaturesdir, sfpkl2)

            if os.path.exists(sfpath1):
                starfeatures_list.append(sfpkl1)
            elif os.path.exists(sfpath2):
                starfeatures_list.append(sfpkl2)
            else:
                starfeatures_list.append(None)

    else:

        starfeatures_list = [None for x in pfpkl_list]

    # generate the task list
    kwargs = {'fourierorder':fourierorder,
              'transitparams':transitparams,
              'ebparams':ebparams,
              'pdiff_threshold':pdiff_threshold,
              'sidereal_threshold':sidereal_threshold,
              'sampling_peak_multiplier':sampling_peak_multiplier,
              'sampling_startp':sampling_startp,
              'sampling_endp':sampling_endp,
              'timecols':timecols,
              'magcols':magcols,
              'errcols':errcols,
              'lcformat':lcformat,
              'lcformatdir':lcformat,
              'sigclip':sigclip,
              'verbose':verbose}

    tasks = [(x, lcbasedir, outdir, y, kwargs) for (x,y) in
             zip(pfpkl_list, starfeatures_list)]

    LOGINFO('processing periodfinding pickles...')

    with ProcessPoolExecutor(max_workers=nworkers) as executor:
        resultfutures = executor.map(_periodicfeatures_worker, tasks)

    results = [x for x in resultfutures]
    resdict = {os.path.basename(x):y for (x,y) in zip(pfpkl_list, results)}

    return resdict