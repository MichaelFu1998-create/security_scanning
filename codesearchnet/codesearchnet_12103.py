def jhk_to_sdssr(jmag,hmag,kmag):
    '''Converts given J, H, Ks mags to an SDSS r magnitude value.

    Parameters
    ----------

    jmag,hmag,kmag : float
        2MASS J, H, Ks mags of the object.

    Returns
    -------

    float
        The converted SDSS r band magnitude.

    '''

    return convert_constants(jmag,hmag,kmag,
                             SDSSR_JHK,
                             SDSSR_JH, SDSSR_JK, SDSSR_HK,
                             SDSSR_J, SDSSR_H, SDSSR_K)