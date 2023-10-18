def absolute_gaia_magnitude(gaia_mag,
                            gaia_parallax_mas,
                            gaia_mag_err=None,
                            gaia_parallax_err_mas=None):
    '''Calculates the GAIA absolute magnitude for object (or array of objects).

    Given a G mag and the parallax measured by GAIA, gets the absolute mag using
    the usual equation::

        G - M_G = 5 x log10(d_pc) - 5
        M_G = 5 - 5log10(d_pc) + G

    Parameters
    ----------

    gaia_mag : float or array-like
        The measured GAIA G magnitude.

    gaia_parallax_max : float or array-like
        The measured parallax of the object in mas.

    gaia_mag_err : float or array-like or None
        The measurement error in GAIA G magnitude.

    gaia_parallax_err_mas : float or array-like or None
        The measurement error in GAIA parallax in mas.

    Returns
    -------

    float or array-like
        The absolute magnitude M_G of the object(s).

    If both `_err` input kwargs are provided, will return a tuple of the form::

        (M_G float or array-like, M_G_err float or array-like)

    '''

    # get the distance
    # we're using the naive calculation of d. this is inaccurate as stated in
    # Bailer-Jones 2015 (http://arxiv.org/abs/1507.02105) if the error in
    # parallax is a significant fraction of parallax
    d_pc = np.abs(1000.0/gaia_parallax_mas)

    # get the distance error
    if gaia_parallax_err_mas is not None:
        d_pc_err = (
            (1000.0/(gaia_parallax_mas*gaia_parallax_mas)) *
            gaia_parallax_err_mas
        )
    else:
        d_pc_err = None

    # calculate the absolute mag from the relation
    # FIXME: this is NOT corrected for extinction in G mag. see Jordi+ 2010
    # (http://adsabs.harvard.edu/abs/2010A%26A...523A..48J) to figure out
    # A_G/A_V as a function of (V-I)_0, then apply it here
    M_G = 5 - 5.0*np.log10(d_pc) + gaia_mag

    # calculate the err in M_G
    if d_pc_err is not None and gaia_mag_err is not None:

        M_G_err = np.sqrt(
            ((5.0/(d_pc * np.log(10.0)))**2 * (d_pc_err)**2) +
            gaia_mag_err*gaia_mag_err
        )
    else:
        M_G_err = None


    if M_G_err is not None:
        return M_G, M_G_err
    else:
        return M_G