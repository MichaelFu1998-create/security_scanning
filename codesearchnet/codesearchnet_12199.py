def runpf(lcfile,
          outdir,
          timecols=None,
          magcols=None,
          errcols=None,
          lcformat='hat-sql',
          lcformatdir=None,
          pfmethods=('gls','pdm','mav','win'),
          pfkwargs=({},{},{},{}),
          sigclip=10.0,
          getblssnr=False,
          nworkers=NCPUS,
          minobservations=500,
          excludeprocessed=False,
          raiseonfail=False):
    '''This runs the period-finding for a single LC.

    Parameters
    ----------

    lcfile : str
        The light curve file to run period-finding on.

    outdir : str
        The output directory where the result pickle will go.

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

    pfmethods : list of str
        This is a list of period finding methods to run. Each element is a
        string matching the keys of the `PFMETHODS` dict above. By default, this
        runs GLS, PDM, AoVMH, and the spectral window Lomb-Scargle periodogram.

    pfkwargs : list of dicts
        This is used to provide any special kwargs as dicts to each
        period-finding method function specified in `pfmethods`.

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

    getblssnr : bool
        If this is True and BLS is one of the methods specified in `pfmethods`,
        will also calculate the stats for each best period in the BLS results:
        transit depth, duration, ingress duration, refit period and epoch, and
        the SNR of the transit.

    nworkers : int
        The number of parallel period-finding workers to launch.

    minobservations : int
        The minimum number of finite LC points required to process a light
        curve.

    excludeprocessed : bool
        If this is True, light curves that have existing period-finding result
        pickles in `outdir` will not be processed.

        FIXME: currently, this uses a dumb method of excluding already-processed
        files. A smarter way to do this is to (i) generate a SHA512 cachekey
        based on a repr of `{'lcfile', 'timecols', 'magcols', 'errcols',
        'lcformat', 'pfmethods', 'sigclip', 'getblssnr', 'pfkwargs'}`, (ii) make
        sure all list kwargs in the dict are sorted, (iii) check if the output
        file has the same cachekey in its filename (last 8 chars of cachekey
        should work), so the result was processed in exactly the same way as
        specifed in the input to this function, and can therefore be
        ignored. Will implement this later.

    raiseonfail : bool
        If something fails and this is True, will raise an Exception instead of
        returning None at the end.

    Returns
    -------

    str
        The path to the output period-finding result pickle.

    '''

    try:
        formatinfo = get_lcformat(lcformat,
                                  use_lcformat_dir=lcformatdir)
        if formatinfo:
            (dfileglob, readerfunc,
             dtimecols, dmagcols, derrcols,
             magsarefluxes, normfunc) = formatinfo
        else:
            LOGERROR("can't figure out the light curve format")
            return None
    except Exception as e:
        LOGEXCEPTION("can't figure out the light curve format")
        return None

    # override the default timecols, magcols, and errcols
    # using the ones provided to the function
    if timecols is None:
        timecols = dtimecols
    if magcols is None:
        magcols = dmagcols
    if errcols is None:
        errcols = derrcols

    try:

        # get the LC into a dict
        lcdict = readerfunc(lcfile)

        # this should handle lists/tuples being returned by readerfunc
        # we assume that the first element is the actual lcdict
        # FIXME: figure out how to not need this assumption
        if ( (isinstance(lcdict, (list, tuple))) and
             (isinstance(lcdict[0], dict)) ):
            lcdict = lcdict[0]

        outfile = os.path.join(outdir, 'periodfinding-%s.pkl' %
                               squeeze(lcdict['objectid']).replace(' ', '-'))

        # if excludeprocessed is True, return the output file if it exists and
        # has a size that is at least 100 kilobytes (this should be enough to
        # contain the minimal results of this function).
        if excludeprocessed:

            test_outfile = os.path.exists(outfile)
            test_outfile_gz = os.path.exists(outfile+'.gz')

            if (test_outfile and os.stat(outfile).st_size > 102400):

                LOGWARNING('periodfinding result for %s already exists at %s, '
                           'skipping because excludeprocessed=True'
                           % (lcfile, outfile))
                return outfile

            elif (test_outfile_gz and os.stat(outfile+'.gz').st_size > 102400):

                LOGWARNING(
                    'gzipped periodfinding result for %s already '
                    'exists at %s, skipping because excludeprocessed=True'
                    % (lcfile, outfile+'.gz')
                )
                return outfile+'.gz'


        # this is the final returndict
        resultdict = {
            'objectid':lcdict['objectid'],
            'lcfbasename':os.path.basename(lcfile),
            'kwargs':{'timecols':timecols,
                      'magcols':magcols,
                      'errcols':errcols,
                      'lcformat':lcformat,
                      'lcformatdir':lcformatdir,
                      'pfmethods':pfmethods,
                      'pfkwargs':pfkwargs,
                      'sigclip':sigclip,
                      'getblssnr':getblssnr}
        }

        # normalize using the special function if specified
        if normfunc is not None:
            lcdict = normfunc(lcdict)

        for tcol, mcol, ecol in zip(timecols, magcols, errcols):

            # dereference the columns and get them from the lcdict
            if '.' in tcol:
                tcolget = tcol.split('.')
            else:
                tcolget = [tcol]
            times = _dict_get(lcdict, tcolget)

            if '.' in mcol:
                mcolget = mcol.split('.')
            else:
                mcolget = [mcol]
            mags = _dict_get(lcdict, mcolget)

            if '.' in ecol:
                ecolget = ecol.split('.')
            else:
                ecolget = [ecol]
            errs = _dict_get(lcdict, ecolget)


            # normalize here if not using special normalization
            if normfunc is None:
                ntimes, nmags = normalize_magseries(
                    times, mags,
                    magsarefluxes=magsarefluxes
                )

                times, mags, errs = ntimes, nmags, errs


            # run each of the requested period-finder functions
            resultdict[mcol] = {}

            # check if we have enough non-nan observations to proceed
            finmags = mags[np.isfinite(mags)]

            if finmags.size < minobservations:

                LOGERROR('not enough non-nan observations for '
                         'this LC. have: %s, required: %s, '
                         'magcol: %s, skipping...' %
                         (finmags.size, minobservations, mcol))
                continue

            pfmkeys = []

            for pfmind, pfm, pfkw in zip(range(len(pfmethods)),
                                         pfmethods,
                                         pfkwargs):

                pf_func = PFMETHODS[pfm]

                # get any optional kwargs for this function
                pf_kwargs = pfkw
                pf_kwargs.update({'verbose':False,
                                  'nworkers':nworkers,
                                  'magsarefluxes':magsarefluxes,
                                  'sigclip':sigclip})

                # we'll always prefix things with their index to allow multiple
                # invocations and results from the same period-finder (for
                # different period ranges, for example).
                pfmkey = '%s-%s' % (pfmind, pfm)
                pfmkeys.append(pfmkey)

                # run this period-finder and save its results to the output dict
                resultdict[mcol][pfmkey] = pf_func(
                    times, mags, errs,
                    **pf_kwargs
                )


            #
            # done with running the period finders
            #
            # append the pfmkeys list to the magcol dict
            resultdict[mcol]['pfmethods'] = pfmkeys

            # check if we need to get the SNR from any BLS pfresults
            if 'bls' in pfmethods and getblssnr:

                # we need to scan thru the pfmethods to get to any BLS pfresults
                for pfmk in resultdict[mcol]['pfmethods']:

                    if 'bls' in pfmk:

                        try:

                            bls = resultdict[mcol][pfmk]

                            # calculate the SNR for the BLS as well
                            blssnr = bls_snr(bls, times, mags, errs,
                                             magsarefluxes=magsarefluxes,
                                             verbose=False)

                            # add the SNR results to the BLS result dict
                            resultdict[mcol][pfmk].update({
                                'snr':blssnr['snr'],
                                'transitdepth':blssnr['transitdepth'],
                                'transitduration':blssnr['transitduration'],
                            })

                            # update the BLS result dict with the refit periods
                            # and epochs using the results from bls_snr
                            resultdict[mcol][pfmk].update({
                                'nbestperiods':blssnr['period'],
                                'epochs':blssnr['epoch']
                            })

                        except Exception as e:

                            LOGEXCEPTION('could not calculate BLS SNR for %s' %
                                         lcfile)
                            # add the SNR null results to the BLS result dict
                            resultdict[mcol][pfmk].update({
                                'snr':[np.nan,np.nan,np.nan,np.nan,np.nan],
                                'transitdepth':[np.nan,np.nan,np.nan,
                                                np.nan,np.nan],
                                'transitduration':[np.nan,np.nan,np.nan,
                                                   np.nan,np.nan],
                            })

            elif 'bls' in pfmethods:

                # we need to scan thru the pfmethods to get to any BLS pfresults
                for pfmk in resultdict[mcol]['pfmethods']:

                    if 'bls' in pfmk:

                        # add the SNR null results to the BLS result dict
                        resultdict[mcol][pfmk].update({
                            'snr':[np.nan,np.nan,np.nan,np.nan,np.nan],
                            'transitdepth':[np.nan,np.nan,np.nan,
                                            np.nan,np.nan],
                            'transitduration':[np.nan,np.nan,np.nan,
                                               np.nan,np.nan],
                        })


        # once all mag cols have been processed, write out the pickle
        with open(outfile, 'wb') as outfd:
            pickle.dump(resultdict, outfd, protocol=pickle.HIGHEST_PROTOCOL)

        return outfile

    except Exception as e:

        LOGEXCEPTION('failed to run for %s, because: %s' % (lcfile, e))

        if raiseonfail:
            raise

        return None