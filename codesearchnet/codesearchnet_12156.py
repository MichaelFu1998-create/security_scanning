def keplermag_to_sdssr(keplermag, kic_sdssg, kic_sdssr):
    '''Converts magnitude measurements in Kepler band to SDSS r band.

    Parameters
    ----------

    keplermag : float or array-like
        The Kepler magnitude value(s) to convert to fluxes.

    kic_sdssg,kic_sdssr : float or array-like
        The SDSS g and r magnitudes of the object(s) from the Kepler Input
        Catalog. The .llc.fits MAST light curve file for a Kepler object
        contains these values in the FITS extension 0 header.

    Returns
    -------

    float or array-like
        SDSS r band magnitude(s) converted from the Kepler band magnitude.

    '''
    kic_sdssgr = kic_sdssg - kic_sdssr

    if kic_sdssgr < 0.8:
        kepsdssr = (keplermag - 0.2*kic_sdssg)/0.8
    else:
        kepsdssr = (keplermag - 0.1*kic_sdssg)/0.9
    return kepsdssr