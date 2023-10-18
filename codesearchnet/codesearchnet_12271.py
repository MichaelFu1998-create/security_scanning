def _reform_templatelc_for_tfa(task):
    '''
    This is a parallel worker that reforms light curves for TFA.

    task[0] = lcfile
    task[1] = lcformat
    task[2] = lcformatdir
    task[3] = timecol
    task[4] = magcol
    task[5] = errcol
    task[6] = timebase
    task[7] = interpolate_type
    task[8] = sigclip

    '''

    try:

        (lcfile, lcformat, lcformatdir,
         tcol, mcol, ecol,
         timebase, interpolate_type, sigclip) = task

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

        # get the LC into a dict
        lcdict = readerfunc(lcfile)

        # this should handle lists/tuples being returned by readerfunc
        # we assume that the first element is the actual lcdict
        # FIXME: figure out how to not need this assumption
        if ( (isinstance(lcdict, (list, tuple))) and
             (isinstance(lcdict[0], dict)) ):
            lcdict = lcdict[0]

        outdict = {}

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

        #
        # now we'll do: 1. sigclip, 2. reform to timebase, 3. renorm to zero
        #

        # 1. sigclip as requested
        stimes, smags, serrs = sigclip_magseries(times,
                                                 mags,
                                                 errs,
                                                 sigclip=sigclip)

        # 2. now, we'll renorm to the timebase
        mags_interpolator = spi.interp1d(stimes, smags,
                                         kind=interpolate_type,
                                         fill_value='extrapolate')
        errs_interpolator = spi.interp1d(stimes, serrs,
                                         kind=interpolate_type,
                                         fill_value='extrapolate')

        interpolated_mags = mags_interpolator(timebase)
        interpolated_errs = errs_interpolator(timebase)

        # 3. renorm to zero
        magmedian = np.median(interpolated_mags)

        renormed_mags = interpolated_mags - magmedian

        # update the dict
        outdict = {'mags':renormed_mags,
                   'errs':interpolated_errs,
                   'origmags':interpolated_mags}

        #
        # done with this magcol
        #
        return outdict

    except Exception as e:

        LOGEXCEPTION('reform LC task failed: %s' % repr(task))
        return None