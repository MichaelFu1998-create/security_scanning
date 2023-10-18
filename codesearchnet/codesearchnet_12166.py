def rfepd_kepler_lightcurve(
        lcdict,
        xccol='mom_centr1',
        yccol='mom_centr2',
        timestoignore=None,
        filterflags=True,
        writetodict=True,
        epdsmooth=23,
        decorr='xcc,ycc',
        nrftrees=200
):
    '''This uses a `RandomForestRegressor` to fit and decorrelate Kepler light
    curves.

    Fits the X and Y positions, the background, and background error.

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

            rfepd_time = time array
            rfepd_sapflux = uncorrected flux before EPD
            rfepd_epdsapflux = corrected flux after EPD
            rfepd_epdsapcorr = EPD flux corrections
            rfepd_bkg = background array
            rfepd_bkg_err = background errors array
            rfepd_xcc = xcoord array
            rfepd_ycc = ycoord array
            rfepd_quality = quality flag array

        and updates the 'columns' list in the lcdict as well.

    epdsmooth : int
        Sets the number of light curve points to smooth over when generating the
        EPD fit function.

    decorr : {'xcc,ycc','bgv,bge','xcc,ycc,bgv,bge'}
        Indicates whether to use the x,y coords alone; background value and
        error alone; or x,y coords and background value, error in combination as
        the features to training the `RandomForestRegressor` on and perform the
        fit.

    nrftrees : int
        The number of trees to use in the `RandomForestRegressor`.

    Returns
    -------

    tuple
        Returns a tuple of the form: (times, corrected_fluxes, flux_corrections)

    '''

    times, fluxes, background, background_err = (
        lcdict['time'],
        lcdict['sap']['sap_flux'],
        lcdict['sap']['sap_bkg'],
        lcdict['sap']['sap_bkg_err']
    )
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
        LOGINFO('applied quality flag filter, ndet before = %s, '
                'ndet after = %s'
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

    # set up the regressor
    RFR = RandomForestRegressor(n_estimators=nrftrees)

    if decorr == 'xcc,ycc,bgv,bge':
        # collect the features and target variable
        features = npcolumn_stack((xcc,ycc,background,background_err))
    elif decorr == 'xcc,ycc':
        # collect the features and target variable
        features = npcolumn_stack((xcc,ycc))
    elif decorr == 'bgv,bge':
        # collect the features and target variable
        features = npcolumn_stack((background,background_err))
    else:
        LOGERROR("couldn't understand decorr, not decorrelating...")
        return None

    # smooth the light curve
    if epdsmooth:
        smoothedfluxes = median_filter(fluxes, size=epdsmooth)
    else:
        smoothedfluxes = fluxes

    # fit, then generate the predicted values, then get corrected values
    RFR.fit(features, smoothedfluxes)
    flux_corrections = RFR.predict(features)
    corrected_fluxes = npmedian(fluxes) + fluxes - flux_corrections

    # remove the random forest to save RAM
    del RFR

    # write these to the dictionary if requested
    if writetodict:

        lcdict['rfepd'] = {}
        lcdict['rfepd']['time'] = times
        lcdict['rfepd']['sapflux'] = fluxes
        lcdict['rfepd']['epdsapflux'] = corrected_fluxes
        lcdict['rfepd']['epdsapcorr'] = flux_corrections
        lcdict['rfepd']['bkg'] = background
        lcdict['rfepd']['bkg_err'] = background_err
        lcdict['rfepd']['xcc'] = xcc
        lcdict['rfepd']['ycc'] = ycc
        lcdict['rfepd']['quality'] = flags

        for newcol in ['rfepd.time','rfepd.sapflux',
                       'rfepd.epdsapflux','rfepd.epdsapcorr',
                       'rfepd.bkg','rfepd.bkg.err',
                       'rfepd.xcc','rfepd.ycc',
                       'rfepd.quality']:

            if newcol not in lcdict['columns']:
                lcdict['columns'].append(newcol)

    return times, corrected_fluxes, flux_corrections