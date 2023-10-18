def get_time_flux_errs_from_Ames_lightcurve(infile,
                                            lctype,
                                            cadence_min=2):
    '''Reads TESS Ames-format FITS light curve files.

    MIT TOI alerts include Ames lightcurve files. This function gets the finite,
    nonzero times, fluxes, and errors with QUALITY == 0.

    NOTE: the PDCSAP lightcurve typically still need "pre-whitening" after this
    step.

    .. deprecated:: 0.3.20
        This function will be removed in astrobase v0.4.2. Use the
        `read_tess_fitslc` and `consolidate_tess_fitslc` functions instead.

    Parameters
    ----------

    infile : str
        The path to `*.fits.gz` TOI alert file, from Ames pipeline.

    lctype : {'PDCSAP','SAP'}
        The type of light curve to extract from the FITS LC file.

    cadence_min : int
        The expected frame cadence in units of minutes. Raises ValueError if you
        use the wrong cadence.

    Returns
    -------

    tuple
        The tuple returned is of the form:

        (times, normalized (to median) fluxes, flux errors)

    '''

    warnings.warn(
        "Use the astrotess.read_tess_fitslc and "
        "astrotess.consolidate_tess_fitslc functions instead of this function. "
        "This function will be removed in astrobase v0.4.2.",
        FutureWarning
    )

    if lctype not in ('PDCSAP','SAP'):
        raise ValueError('unknown light curve type requested: %s' % lctype)

    hdulist = pyfits.open(infile)

    main_hdr = hdulist[0].header
    lc_hdr = hdulist[1].header
    lc = hdulist[1].data

    if (('Ames' not in main_hdr['ORIGIN']) or
        ('LIGHTCURVE' not in lc_hdr['EXTNAME'])):
        raise ValueError(
            'could not understand input LC format. '
            'Is it a TESS TOI LC file?'
        )

    time = lc['TIME']
    flux = lc['{:s}_FLUX'.format(lctype)]
    err_flux = lc['{:s}_FLUX_ERR'.format(lctype)]

    # REMOVE POINTS FLAGGED WITH:
    # attitude tweaks, safe mode, coarse/earth pointing, argabrithening events,
    # reaction wheel desaturation events, cosmic rays in optimal aperture
    # pixels, manual excludes, discontinuities, stray light from Earth or Moon
    # in camera FoV.
    # (Note: it's not clear to me what a lot of these mean. Also most of these
    # columns are probably not correctly propagated right now.)
    sel = (lc['QUALITY'] == 0)
    sel &= np.isfinite(time)
    sel &= np.isfinite(flux)
    sel &= np.isfinite(err_flux)
    sel &= ~np.isnan(time)
    sel &= ~np.isnan(flux)
    sel &= ~np.isnan(err_flux)
    sel &= (time != 0)
    sel &= (flux != 0)
    sel &= (err_flux != 0)

    time = time[sel]
    flux = flux[sel]
    err_flux = err_flux[sel]

    # ensure desired cadence
    lc_cadence_diff = np.abs(np.nanmedian(np.diff(time))*24*60 - cadence_min)

    if lc_cadence_diff > 1.0e-2:
        raise ValueError(
            'the light curve is not at the required cadence specified: %.2f' %
            cadence_min
        )

    fluxmedian = np.nanmedian(flux)
    flux /= fluxmedian
    err_flux /= fluxmedian

    return time, flux, err_flux