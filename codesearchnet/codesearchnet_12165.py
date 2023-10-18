def epd_kepler_lightcurve(lcdict,
                          xccol='mom_centr1',
                          yccol='mom_centr2',
                          timestoignore=None,
                          filterflags=True,
                          writetodict=True,
                          epdsmooth=5):
    '''This runs EPD on the Kepler light curve.

    Following Huang et al. 2015, we fit the following EPD function to a smoothed
    light curve, and then subtract it to obtain EPD corrected magnitudes::

        f = c0 +
            c1*sin(2*pi*x) + c2*cos(2*pi*x) + c3*sin(2*pi*y) + c4*cos(2*pi*y) +
            c5*sin(4*pi*x) + c6*cos(4*pi*x) + c7*sin(4*pi*y) + c8*cos(4*pi*y) +
            c9*bgv + c10*bge

    By default, this function removes points in the Kepler LC that have ANY
    quality flags set.

    Parameters
    ----------

    lcdict : lcdict
        An `lcdict` produced by `consolidate_kepler_fitslc` or
        `read_kepler_fitslc`.

    xcol,ycol : str
        Indicates the x and y coordinate column names to use from the Kepler LC
        in the EPD fit.

    timestoignore : list of tuples
        This is of the form::

            [(time1_start, time1_end), (time2_start, time2_end), ...]

        and indicates the start and end times to mask out of the final
        lcdict. Use this to remove anything that wasn't caught by the quality
        flags.

    filterflags : bool
        If True, will remove any measurements that have non-zero quality flags
        present. This usually indicates an issue with the instrument or
        spacecraft.

    writetodict : bool
        If writetodict is True, adds the following columns to the lcdict::

            epd_time = time array
            epd_sapflux = uncorrected flux before EPD
            epd_epdsapflux = corrected flux after EPD
            epd_epdsapcorr = EPD flux corrections
            epd_bkg = background array
            epd_bkg_err = background errors array
            epd_xcc = xcoord array
            epd_ycc = ycoord array
            epd_quality = quality flag array

        and updates the 'columns' list in the lcdict as well.

    epdsmooth : int
        Sets the number of light curve points to smooth over when generating the
        EPD fit function.

    Returns
    -------

    tuple
        Returns a tuple of the form: (times, epdfluxes, fitcoeffs, epdfit)

    '''

    times, fluxes, background, background_err = (lcdict['time'],
                                                 lcdict['sap']['sap_flux'],
                                                 lcdict['sap']['sap_bkg'],
                                                 lcdict['sap']['sap_bkg_err'])
    xcc = lcdict[xccol]
    ycc = lcdict[yccol]
    flags = lcdict['sap_quality']

    # filter all bad LC points as noted by quality flags
    if filterflags:

        nbefore = times.size

        filterind = flags == 0

        times = times[filterind]
        fluxes = fluxes[filterind]
        background = background[filterind]
        background_err = background_err[filterind]
        xcc = xcc[filterind]
        ycc = ycc[filterind]
        flags = flags[filterind]

        nafter = times.size
        LOGINFO('applied quality flag filter, ndet before = %s, ndet after = %s'
                % (nbefore, nafter))


    # remove nans
    find = (npisfinite(xcc) & npisfinite(ycc) &
            npisfinite(times) & npisfinite(fluxes) &
            npisfinite(background) & npisfinite(background_err))

    nbefore = times.size

    times = times[find]
    fluxes = fluxes[find]
    background = background[find]
    background_err = background_err[find]
    xcc = xcc[find]
    ycc = ycc[find]
    flags = flags[find]

    nafter = times.size
    LOGINFO('removed nans, ndet before = %s, ndet after = %s'
            % (nbefore, nafter))


    # exclude all times in timestoignore
    if (timestoignore and
        isinstance(timestoignore, list) and
        len(timestoignore) > 0):

        exclind = npfull_like(times,True)
        nbefore = times.size

        # apply all the masks
        for ignoretime in timestoignore:
            time0, time1 = ignoretime[0], ignoretime[1]
            thismask = (times > time0) & (times < time1)
            exclind = exclind & thismask

        # quantities after masks have been applied
        times = times[exclind]
        fluxes = fluxes[exclind]
        background = background[exclind]
        background_err = background_err[exclind]
        xcc = xcc[exclind]
        ycc = ycc[exclind]
        flags = flags[exclind]

        nafter = times.size
        LOGINFO('removed timestoignore, ndet before = %s, ndet after = %s'
                % (nbefore, nafter))


    # now that we're all done, we can do EPD
    # first, smooth the light curve
    smoothedfluxes = median_filter(fluxes, size=epdsmooth)

    # initial fit coeffs
    initcoeffs = npones(11)

    # fit the the smoothed mags and find better coeffs
    leastsqfit = leastsq(_epd_residual,
                         initcoeffs,
                         args=(smoothedfluxes,
                               xcc, ycc,
                               background, background_err))

    # if the fit succeeds, then get the EPD fluxes
    if leastsqfit[-1] in (1,2,3,4):

        fitcoeffs = leastsqfit[0]
        epdfit = _epd_function(fitcoeffs,
                               fluxes,
                               xcc,
                               ycc,
                               background,
                               background_err)
        epdfluxes = npmedian(fluxes) + fluxes - epdfit

        # write these to the dictionary if requested
        if writetodict:

            lcdict['epd'] = {}

            lcdict['epd']['time'] = times
            lcdict['epd']['sapflux'] = fluxes
            lcdict['epd']['epdsapflux'] = epdfluxes
            lcdict['epd']['epdsapcorr'] = epdfit
            lcdict['epd']['bkg'] = background
            lcdict['epd']['bkg_err'] = background_err
            lcdict['epd']['xcc'] = xcc
            lcdict['epd']['ycc'] = ycc
            lcdict['epd']['quality'] = flags

            for newcol in ['epd.time','epd.sapflux',
                           'epd.epdsapflux','epd.epdsapcorr',
                           'epd.bkg','epd.bkg.err',
                           'epd.xcc','epd.ycc',
                           'epd.quality']:

                if newcol not in lcdict['columns']:
                    lcdict['columns'].append(newcol)

        return times, epdfluxes, fitcoeffs, epdfit

    else:

        LOGERROR('could not fit EPD function to light curve')
        return None, None, None, None