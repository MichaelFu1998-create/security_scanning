def jhk_to_sdssz(jmag,hmag,kmag):
    '''Converts given J, H, Ks mags to an SDSS z magnitude value.

    Parameters
    ----------

    jmag,hmag,kmag : float
        2MASS J, H, Ks mags of the object.

    Returns
    -------

    float
        The converted SDSS z band magnitude.

    '''

    return convert_constants(jmag,hmag,kmag,
                             SDSSZ_JHK,
                             SDSSZ_JH, SDSSZ_JK, SDSSZ_HK,
                             SDSSZ_J, SDSSZ_H, SDSSZ_K)