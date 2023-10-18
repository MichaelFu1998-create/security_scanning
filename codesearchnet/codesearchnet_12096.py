def convert_constants(jmag, hmag, kmag,
                      cjhk,
                      cjh, cjk, chk,
                      cj, ch, ck):
    '''This converts between JHK and BVRI/SDSS mags.

    Not meant to be used directly. See the functions below for more sensible
    interface. This function does the grunt work of converting from JHK to
    either BVRI or SDSS ugriz. while taking care of missing values for any of
    jmag, hmag, or kmag.

    Parameters
    ----------

    jmag,hmag,kmag : float
        2MASS J, H, Ks mags to use to convert.

    cjhk,cjh,cjk,chk,cj,ch,ck : lists
        Constants to use when converting.

    Returns
    -------

    float
        The converted magnitude in SDSS or BVRI system.

    '''

    if jmag is not None:

        if hmag is not None:

            if kmag is not None:

                return cjhk[0] + cjhk[1]*jmag + cjhk[2]*hmag + cjhk[3]*kmag

            else:

                return cjh[0] + cjh[1]*jmag + cjh[2]*hmag

        else:

            if kmag is not None:

                return cjk[0] + cjk[1]*jmag + cjk[2]*kmag

            else:

                return cj[0] + cj[1]*jmag

    else:

        if hmag is not None:

            if kmag is not None:

                return chk[0] + chk[1]*hmag + chk[2]*kmag

            else:

                return ch[0] + ch[1]*hmag

        else:

            if kmag is not None:

                return ck[0] + ck[1]*kmag

            else:

                return np.nan