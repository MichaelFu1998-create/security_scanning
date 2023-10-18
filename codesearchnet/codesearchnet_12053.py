def add_fakelc_variability(fakelcfile,
                           vartype,
                           override_paramdists=None,
                           magsarefluxes=False,
                           overwrite=False):
    '''This adds variability of the specified type to the fake LC.

    The procedure is (for each `magcol`):

    - read the fakelcfile, get the stored moments and vartype info

    - add the periodic variability specified in vartype and varparamdists. if
      `vartype == None`, then do nothing in this step. If `override_vartype` is
      not None, override stored vartype with specified vartype. If
      `override_varparamdists` provided, override with specified
      `varparamdists`. NOTE: the varparamdists must make sense for the vartype,
      otherwise, weird stuff will happen.

    - add the median mag level stored in `fakelcfile` to the time series

    - add Gaussian noise to the light curve as specified in `fakelcfile`

    - add a varinfo key and dict to the lcdict with `varperiod`, `varepoch`,
      `varparams`

    - write back to fake LC pickle

    - return the `varinfo` dict to the caller

    Parameters
    ----------

    fakelcfile : str
        The name of the fake LC file to process.

    vartype : str
        The type of variability to add to this fake LC file.

    override_paramdists : dict
        A parameter distribution dict as in the `generate_XX_lightcurve`
        functions above. If provided, will override the distribution stored in
        the input fake LC file itself.

    magsarefluxes : bool
        Sets if the variability amplitude is in fluxes and not magnitudes.

    overwite : bool
        This overwrites the input fake LC file with a new variable LC even if
        it's been processed before.

    Returns
    -------

    dict
        A dict of the following form is returned::

            {'objectid':lcdict['objectid'],
             'lcfname':fakelcfile,
             'actual_vartype':vartype,
             'actual_varparams':lcdict['actual_varparams']}

    '''

    # read in the fakelcfile
    lcdict = _read_pklc(fakelcfile)

    # make sure to bail out if this light curve already has fake variability
    # added
    if ('actual_vartype' in lcdict and
        'actual_varparams' in lcdict and
        not overwrite):
        LOGERROR('%s has existing variability type: %s '
                 'and params: %s and overwrite = False, '
                 'skipping this file...' %
                 (fakelcfile, lcdict['actual_vartype'],
                  repr(lcdict['actual_varparams'])))
        return None

    # get the times, mags, errs from this LC
    timecols, magcols, errcols = (lcdict['timecols'],
                                  lcdict['magcols'],
                                  lcdict['errcols'])


    # get the correct function to apply variability
    if vartype in VARTYPE_LCGEN_MAP:
        vargenfunc = VARTYPE_LCGEN_MAP[vartype]
    elif vartype is None:
        vargenfunc = None
    else:
        LOGERROR('unknown variability type: %s, choose from: %s' %
                 (vartype, repr(list(VARTYPE_LCGEN_MAP.keys()))))
        return None


    # 1. generate the variability, including the overrides if provided we do
    # this outside the loop below to get the period, etc. distributions once
    # only per object. NOTE: in doing so, we're assuming that the difference
    # between magcols is just additive and the timebases for each magcol are the
    # same; this is not strictly correct
    if vargenfunc is not None:
        if (override_paramdists is not None and
            isinstance(override_paramdists,dict)):

            variablelc = vargenfunc(lcdict[timecols[0]],
                                    paramdists=override_paramdists,
                                    magsarefluxes=magsarefluxes)

        else:

            variablelc = vargenfunc(lcdict[timecols[0]],
                                    magsarefluxes=magsarefluxes)

    # for nonvariables, don't execute vargenfunc, but return a similar dict
    # so we can add the required noise to it
    else:
        variablelc = {'vartype':None,
                      'params':None,
                      'times':lcdict[timecols[0]],
                      'mags':np.full_like(lcdict[timecols[0]], 0.0),
                      'errs':np.full_like(lcdict[timecols[0]], 0.0)}


    # now iterate over the time, mag, err columns
    for tcol, mcol, ecol in zip(timecols, magcols, errcols):

        times, mags, errs = lcdict[tcol], lcdict[mcol], lcdict[ecol]

        # 2. get the moments for this magcol
        mag_median = lcdict['moments'][mcol]['median']
        mag_mad = lcdict['moments'][mcol]['mad']

        # add up to 5 mmag of extra RMS for systematics and red-noise
        mag_rms = mag_mad*1.483

        err_median = lcdict['moments'][ecol]['median']
        err_mad = lcdict['moments'][ecol]['mad']
        err_rms = err_mad*1.483

        # 3. add the median level + gaussian noise
        magnoise = npr.normal(size=variablelc['mags'].size)*mag_rms
        errnoise = npr.normal(size=variablelc['errs'].size)*err_rms

        finalmags = mag_median + (variablelc['mags'] + magnoise)
        finalerrs = err_median + (variablelc['errs'] + errnoise)

        # 4. update these tcol, mcol, ecol values in the lcdict
        lcdict[mcol] = finalmags
        lcdict[ecol] = finalerrs

    #
    # all done with updating mags and errs
    #

    # 5. update the light curve with the variability info
    lcdict['actual_vartype'] = variablelc['vartype']
    lcdict['actual_varparams'] = variablelc['params']

    # these standard keys are set to help out later with characterizing recovery
    # rates by magnitude, period, amplitude, ndet, etc.
    if vartype is not None:
        lcdict['actual_varperiod'] = variablelc['varperiod']
        lcdict['actual_varamplitude'] = variablelc['varamplitude']
    else:
        lcdict['actual_varperiod'] = np.nan
        lcdict['actual_varamplitude'] = np.nan


    # 6. write back, making sure to do it safely
    tempoutf = '%s.%s' % (fakelcfile, md5(npr.bytes(4)).hexdigest()[-8:])
    with open(tempoutf, 'wb') as outfd:
        pickle.dump(lcdict, outfd, pickle.HIGHEST_PROTOCOL)

    if os.path.exists(tempoutf):
        shutil.copy(tempoutf, fakelcfile)
        os.remove(tempoutf)
    else:
        LOGEXCEPTION('could not write output light curve file to dir: %s' %
                     os.path.dirname(tempoutf))
        # fail here
        raise

    LOGINFO('object: %s, vartype: %s -> %s OK' % (
        lcdict['objectid'],
        vartype,
        fakelcfile)
    )

    return {'objectid':lcdict['objectid'],
            'lcfname':fakelcfile,
            'actual_vartype':vartype,
            'actual_varparams':lcdict['actual_varparams']}