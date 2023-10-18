def jhk_to_sdssu(jmag,hmag,kmag):
    '''Converts given J, H, Ks mags to an SDSS u magnitude value.

    Parameters
    ----------

    jmag,hmag,kmag : float
        2MASS J, H, Ks mags of the object.

    Returns
    -------

    float
        The converted SDSS u band magnitude.

    '''

    return convert_constants(jmag,hmag,kmag,
                             SDSSU_JHK,
                             SDSSU_JH, SDSSU_JK, SDSSU_HK,
                             SDSSU_J, SDSSU_H, SDSSU_K)