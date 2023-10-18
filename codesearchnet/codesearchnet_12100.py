def jhk_to_imag(jmag,hmag,kmag):
    '''Converts given J, H, Ks mags to an I magnitude value.

    Parameters
    ----------

    jmag,hmag,kmag : float
        2MASS J, H, Ks mags of the object.

    Returns
    -------

    float
        The converted I band magnitude.

    '''

    return convert_constants(jmag,hmag,kmag,
                             IJHK,
                             IJH, IJK, IHK,
                             IJ, IH, IK)