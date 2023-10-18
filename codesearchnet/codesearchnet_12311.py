def periodicvar_recovery(fakepfpkl,
                         simbasedir,
                         period_tolerance=1.0e-3):

    '''Recovers the periodic variable status/info for the simulated PF result.

    - Uses simbasedir and the lcfbasename stored in fakepfpkl to figure out
      where the LC for this object is.
    - Gets the actual_varparams, actual_varperiod, actual_vartype,
      actual_varamplitude elements from the LC.
    - Figures out if the current objectid is a periodic variable (using
      actual_vartype).
    - If it is a periodic variable, gets the canonical period assigned to it.
    - Checks if the period was recovered in any of the five best periods
      reported by any of the period-finders, checks if the period recovered was
      a harmonic of the period.
    - Returns the objectid, actual period and vartype, recovered period, and
      recovery status.


    Parameters
    ----------

    fakepfpkl : str
        This is a periodfinding-<objectid>.pkl[.gz] file produced in the
        `simbasedir/periodfinding` subdirectory after `run_periodfinding` above
        is done.

    simbasedir : str
        The base directory where all of the fake LCs and period-finding results
        are.

    period_tolerance : float
        The maximum difference that this function will consider between an
        actual period (or its aliases) and a recovered period to consider it as
        as a 'recovered' period.

    Returns
    -------

    dict
        Returns a dict of period-recovery results.

    '''

    if fakepfpkl.endswith('.gz'):
        infd = gzip.open(fakepfpkl,'rb')
    else:
        infd = open(fakepfpkl,'rb')

    fakepf = pickle.load(infd)
    infd.close()

    # get info from the fakepf dict
    objectid, lcfbasename = fakepf['objectid'], fakepf['lcfbasename']
    lcfpath = os.path.join(simbasedir,'lightcurves',lcfbasename)

    # if the LC doesn't exist, bail out
    if not os.path.exists(lcfpath):
        LOGERROR('light curve for %s does not exist at: %s' % (objectid,
                                                               lcfpath))
        return None

    # now, open the fakelc
    fakelc = lcproc._read_pklc(lcfpath)

    # get the actual_varparams, actual_varperiod, actual_varamplitude
    actual_varparams, actual_varperiod, actual_varamplitude, actual_vartype = (
        fakelc['actual_varparams'],
        fakelc['actual_varperiod'],
        fakelc['actual_varamplitude'],
        fakelc['actual_vartype']
    )

    # get the moments too so we can track LC noise, etc.
    actual_moments = fakelc['moments']

    # get the magcols for this LC
    magcols = fakelc['magcols']

    # get the recovered info from each of the available methods
    pfres = {
        'objectid':objectid,
        'simbasedir':simbasedir,
        'magcols':magcols,
        'fakelc':os.path.abspath(lcfpath),
        'fakepf':os.path.abspath(fakepfpkl),
        'actual_vartype':actual_vartype,
        'actual_varperiod':actual_varperiod,
        'actual_varamplitude':actual_varamplitude,
        'actual_varparams':actual_varparams,
        'actual_moments':actual_moments,
        'recovery_periods':[],
        'recovery_lspvals':[],
        'recovery_pfmethods':[],
        'recovery_magcols':[],
        'recovery_status':[],
        'recovery_pdiff':[],
    }

    # populate the pfres dict with the periods, pfmethods, and magcols
    for magcol in magcols:

        for pfm in lcproc.PFMETHODS:

            if pfm in fakepf[magcol]:

                # only get the unique recovered periods by using
                # period_tolerance
                for rpi, rp in enumerate(
                        fakepf[magcol][pfm]['nbestperiods']
                ):

                    if ((not np.any(np.isclose(
                            rp,
                            np.array(pfres['recovery_periods']),
                            rtol=period_tolerance
                    ))) and np.isfinite(rp)):

                        # populate the recovery periods, pfmethods, and magcols
                        pfres['recovery_periods'].append(rp)
                        pfres['recovery_pfmethods'].append(pfm)
                        pfres['recovery_magcols'].append(magcol)

                        # normalize the periodogram peak value to between
                        # 0 and 1 so we can put in the results of multiple
                        # periodfinders on one scale
                        if pfm == 'pdm':

                            this_lspval = (
                                np.max(fakepf[magcol][pfm]['lspvals']) -
                                fakepf[magcol][pfm]['nbestlspvals'][rpi]
                            )

                        else:

                            this_lspval = (
                                fakepf[magcol][pfm]['nbestlspvals'][rpi] /
                                np.max(fakepf[magcol][pfm]['lspvals'])
                            )

                        # add the normalized lspval to the outdict for
                        # this object as well. later, we'll use this to
                        # construct a periodogram for objects that were actually
                        # not variables
                        pfres['recovery_lspvals'].append(this_lspval)


    # convert the recovery_* lists to arrays
    pfres['recovery_periods'] = np.array(pfres['recovery_periods'])
    pfres['recovery_lspvals'] = np.array(pfres['recovery_lspvals'])
    pfres['recovery_pfmethods'] = np.array(pfres['recovery_pfmethods'])
    pfres['recovery_magcols'] = np.array(pfres['recovery_magcols'])

    #
    # now figure out recovery status
    #

    # if this is an actual periodic variable, characterize the recovery
    if (actual_vartype and
        actual_vartype in PERIODIC_VARTYPES and
        np.isfinite(actual_varperiod)):

        if pfres['recovery_periods'].size > 0:

            for ri in range(pfres['recovery_periods'].size):

                pfres['recovery_pdiff'].append(pfres['recovery_periods'][ri] -
                                               np.asscalar(actual_varperiod))

                # get the alias types
                pfres['recovery_status'].append(
                    check_periodrec_alias(actual_varperiod,
                                          pfres['recovery_periods'][ri],
                                          tolerance=period_tolerance)
                )

            # turn the recovery_pdiff/status lists into arrays
            pfres['recovery_status'] = np.array(pfres['recovery_status'])
            pfres['recovery_pdiff'] = np.array(pfres['recovery_pdiff'])

            # find the best recovered period and its status
            rec_absdiff = np.abs(pfres['recovery_pdiff'])
            best_recp_ind = rec_absdiff == rec_absdiff.min()

            pfres['best_recovered_period'] = (
                pfres['recovery_periods'][best_recp_ind]
            )
            pfres['best_recovered_pfmethod'] = (
                pfres['recovery_pfmethods'][best_recp_ind]
            )
            pfres['best_recovered_magcol'] = (
                pfres['recovery_magcols'][best_recp_ind]
            )
            pfres['best_recovered_status'] = (
                pfres['recovery_status'][best_recp_ind]
            )
            pfres['best_recovered_pdiff'] = (
                pfres['recovery_pdiff'][best_recp_ind]
            )

        else:

            LOGWARNING(
                'no finite periods recovered from period-finding for %s' %
                fakepfpkl
            )

            pfres['recovery_status'] = np.array(['no_finite_periods_recovered'])
            pfres['recovery_pdiff'] = np.array([np.nan])
            pfres['best_recovered_period'] = np.array([np.nan])
            pfres['best_recovered_pfmethod'] = np.array([],dtype=np.unicode_)
            pfres['best_recovered_magcol'] = np.array([],dtype=np.unicode_)
            pfres['best_recovered_status'] = np.array([],dtype=np.unicode_)
            pfres['best_recovered_pdiff'] = np.array([np.nan])

    # if this is not actually a variable, get the recovered period,
    # etc. anyway. this way, we can see what we need to look out for and avoid
    # when getting these values for actual objects
    else:

        pfres['recovery_status'] = np.array(
            ['not_variable']*pfres['recovery_periods'].size
        )
        pfres['recovery_pdiff'] = np.zeros(pfres['recovery_periods'].size)

        pfres['best_recovered_period'] = np.array([np.nan])
        pfres['best_recovered_pfmethod'] = np.array([],dtype=np.unicode_)
        pfres['best_recovered_magcol'] = np.array([],dtype=np.unicode_)
        pfres['best_recovered_status'] = np.array(['not_variable'])
        pfres['best_recovered_pdiff'] = np.array([np.nan])

    return pfres