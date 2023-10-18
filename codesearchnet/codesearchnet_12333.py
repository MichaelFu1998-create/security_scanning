def jd_corr(jd,
            ra, dec,
            obslon=None,
            obslat=None,
            obsalt=None,
            jd_type='bjd'):
    '''Returns BJD_TDB or HJD_TDB for input JD_UTC.

    The equation used is::

        BJD_TDB = JD_UTC + JD_to_TDB_corr + romer_delay

    where:

    - JD_to_TDB_corr is the difference between UTC and TDB JDs
    - romer_delay is the delay caused by finite speed of light from Earth-Sun

    This is based on the code at:

    https://mail.scipy.org/pipermail/astropy/2014-April/003148.html

    Note that this does not correct for:

    1. precession of coordinates if the epoch is not 2000.0
    2. precession of coordinates if the target has a proper motion
    3. Shapiro delay
    4. Einstein delay

    Parameters
    ----------

    jd : float or array-like
        The Julian date(s) measured at UTC.

    ra,dec : float
        The equatorial coordinates of the object in decimal degrees.

    obslon,obslat,obsalt : float or None
        The longitude, latitude of the observatory in decimal degrees and
        altitude of the observatory in meters. If these are not provided, the
        corrected JD will be calculated with respect to the center of the Earth.

    jd_type : {'bjd','hjd'}
        Conversion type to perform, either to Baryocentric Julian Date ('bjd')
        or to Heliocenter Julian Date ('hjd').

    Returns
    -------

    float or np.array
        The converted BJD or HJD.

    '''

    if not HAVEKERNEL:
        LOGERROR('no JPL kernel available, can\'t continue!')
        return

    # Source unit-vector
    ## Assume coordinates in ICRS
    ## Set distance to unit (kilometers)

    # convert the angles to degrees
    rarad = np.radians(ra)
    decrad = np.radians(dec)
    cosra = np.cos(rarad)
    sinra = np.sin(rarad)
    cosdec = np.cos(decrad)
    sindec = np.sin(decrad)

    # this assumes that the target is very far away
    src_unitvector = np.array([cosdec*cosra,cosdec*sinra,sindec])

    # Convert epochs to astropy.time.Time
    ## Assume JD(UTC)
    if (obslon is None) or (obslat is None) or (obsalt is None):
        t = astime.Time(jd, scale='utc', format='jd')
    else:
        t = astime.Time(jd, scale='utc', format='jd',
                        location=('%.5fd' % obslon,
                                  '%.5fd' % obslat,
                                  obsalt))

    # Get Earth-Moon barycenter position
    ## NB: jplephem uses Barycentric Dynamical Time, e.g. JD(TDB)
    ## and gives positions relative to solar system barycenter
    barycenter_earthmoon = jplkernel[0,3].compute(t.tdb.jd)

    # Get Moon position vectors from the center of Earth to the Moon
    # this means we get the following vectors from the ephemerides
    # Earth Barycenter (3) -> Moon (301)
    # Earth Barycenter (3) -> Earth (399)
    # so the final vector is [3,301] - [3,399]
    # units are in km
    moonvector = (jplkernel[3,301].compute(t.tdb.jd) -
                  jplkernel[3,399].compute(t.tdb.jd))

    # Compute Earth position vectors (this is for the center of the earth with
    # respect to the solar system barycenter)
    # all these units are in km
    pos_earth = (barycenter_earthmoon - moonvector * 1.0/(1.0+EMRAT))

    if jd_type == 'bjd':

        # Compute BJD correction
        ## Assume source vectors parallel at Earth and Solar System
        ## Barycenter
        ## i.e. source is at infinity
        # the romer_delay correction is (r.dot.n)/c where:
        # r is the vector from SSB to earth center
        # n is the unit vector from
        correction_seconds = np.dot(pos_earth.T, src_unitvector)/CLIGHT_KPS
        correction_days = correction_seconds/SEC_P_DAY

    elif jd_type == 'hjd':

        # Compute HJD correction via Sun ephemeris

        # this is the position vector of the center of the sun in km
        # Solar System Barycenter (0) -> Sun (10)
        pos_sun = jplkernel[0,10].compute(t.tdb.jd)

        # this is the vector from the center of the sun to the center of the
        # earth
        sun_earth_vec = pos_earth - pos_sun

        # calculate the heliocentric correction
        correction_seconds = np.dot(sun_earth_vec.T, src_unitvector)/CLIGHT_KPS
        correction_days = correction_seconds/SEC_P_DAY

    # TDB is the appropriate time scale for these ephemerides
    new_jd = t.tdb.jd + correction_days

    return new_jd