def precess_coordinates(ra, dec,
                        epoch_one, epoch_two,
                        jd=None,
                        mu_ra=0.0,
                        mu_dec=0.0,
                        outscalar=False):
    '''Precesses target coordinates `ra`, `dec` from `epoch_one` to `epoch_two`.

    This takes into account the jd of the observations, as well as the proper
    motion of the target mu_ra, mu_dec. Adapted from J. D. Hartman's
    VARTOOLS/converttime.c [coordprecess].

    Parameters
    ----------

    ra,dec : float
        The equatorial coordinates of the object at `epoch_one` to precess in
        decimal degrees.

    epoch_one : float
        Origin epoch to precess from to target epoch. This is a float, like:
        1985.0, 2000.0, etc.

    epoch_two : float
        Target epoch to precess from origin epoch. This is a float, like:
        2000.0, 2018.0, etc.

    jd : float
        The full Julian date to use along with the propermotions in `mu_ra`, and
        `mu_dec` to handle proper motion along with the coordinate frame
        precession. If one of `jd`, `mu_ra`, or `mu_dec` is missing, the proper
        motion will not be used to calculate the final precessed coordinates.

    mu_ra,mu_dec : float
        The proper motion in mas/yr in right ascension and declination. If these
        are provided along with `jd`, the total proper motion of the object will
        be taken into account to calculate the final precessed coordinates.

    outscalar : bool
        If True, converts the output coordinates from one-element np.arrays to
        scalars.

    Returns
    -------

    precessed_ra, precessed_dec : float
        A tuple of precessed equatorial coordinates in decimal degrees at
        `epoch_two` taking into account proper motion if `jd`, `mu_ra`, and
        `mu_dec` are provided.

    '''

    raproc, decproc = np.radians(ra), np.radians(dec)

    if ((mu_ra != 0.0) and (mu_dec != 0.0) and jd):

        jd_epoch_one = JD2000 + (epoch_one - epoch_two)*365.25
        raproc = (
            raproc +
            (jd - jd_epoch_one)*mu_ra*MAS_P_YR_TO_RAD_P_DAY/np.cos(decproc)
        )
        decproc = decproc + (jd - jd_epoch_one)*mu_dec*MAS_P_YR_TO_RAD_P_DAY

    ca = np.cos(raproc)
    cd = np.cos(decproc)
    sa = np.sin(raproc)
    sd = np.sin(decproc)

    if epoch_one != epoch_two:

        t1 = 1.0e-3 * (epoch_two - epoch_one)
        t2 = 1.0e-3 * (epoch_one - 2000.0)

        a = ( t1*ARCSEC_TO_RADIANS * (23062.181 + t2*(139.656 + 0.0139*t2) +
                                      t1*(30.188 - 0.344*t2+17.998*t1)) )
        b = t1*t1*ARCSEC_TO_RADIANS*(79.280 + 0.410*t2 + 0.205*t1) + a
        c = (
            ARCSEC_TO_RADIANS*t1*(20043.109 - t2*(85.33 + 0.217*t2) +
                                  t1*(-42.665 - 0.217*t2 - 41.833*t2))
        )
        sina, sinb, sinc = np.sin(a), np.sin(b), np.sin(c)
        cosa, cosb, cosc = np.cos(a), np.cos(b), np.cos(c)

        precmatrix = np.matrix([[cosa*cosb*cosc - sina*sinb,
                                 sina*cosb + cosa*sinb*cosc,
                                 cosa*sinc],
                                [-cosa*sinb - sina*cosb*cosc,
                                 cosa*cosb - sina*sinb*cosc,
                                 -sina*sinc],
                                [-cosb*sinc,
                                 -sinb*sinc,
                                 cosc]])

        precmatrix = precmatrix.transpose()

        x = (np.matrix([cd*ca, cd*sa, sd])).transpose()

        x2 = precmatrix * x

        outra = np.arctan2(x2[1],x2[0])
        outdec = np.arcsin(x2[2])


        outradeg = np.rad2deg(outra)
        outdecdeg = np.rad2deg(outdec)

        if outradeg < 0.0:
            outradeg = outradeg + 360.0

        if outscalar:
            return float(outradeg), float(outdecdeg)
        else:
            return outradeg, outdecdeg

    else:

        # if the epochs are the same and no proper motion, this will be the same
        # as the input values. if the epochs are the same, but there IS proper
        # motion (and a given JD), then these will be perturbed from the input
        # values of ra, dec by the appropriate amount of motion
        return np.degrees(raproc), np.degrees(decproc)