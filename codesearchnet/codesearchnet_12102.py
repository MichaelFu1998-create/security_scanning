def jhk_to_sdssg(jmag,hmag,kmag):
    '''Converts given J, H, Ks mags to an SDSS g magnitude value.

    Parameters
    ----------

    jmag,hmag,kmag : float
        2MASS J, H, Ks mags of the object.

    Returns
    -------

    float
        The converted SDSS g band magnitude.

    '''

    return convert_constants(jmag,hmag,kmag,
                             SDSSG_JHK,
                             SDSSG_JH, SDSSG_JK, SDSSG_HK,
                             SDSSG_J, SDSSG_H, SDSSG_K)