def jhk_to_sdssi(jmag,hmag,kmag):
    '''Converts given J, H, Ks mags to an SDSS i magnitude value.

    Parameters
    ----------

    jmag,hmag,kmag : float
        2MASS J, H, Ks mags of the object.

    Returns
    -------

    float
        The converted SDSS i band magnitude.

    '''

    return convert_constants(jmag,hmag,kmag,
                             SDSSI_JHK,
                             SDSSI_JH, SDSSI_JK, SDSSI_HK,
                             SDSSI_J, SDSSI_H, SDSSI_K)