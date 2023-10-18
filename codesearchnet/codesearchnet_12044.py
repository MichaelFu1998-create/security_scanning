def xieta_from_radecl(inra, indecl,
                      incenterra, incenterdecl,
                      deg=True):
    '''This returns the image-plane projected xi-eta coords for inra, indecl.

    Parameters
    ----------

    inra,indecl : array-like
        The equatorial coordinates to get the xi, eta coordinates for in decimal
        degrees or radians.

    incenterra,incenterdecl : float
        The center coordinate values to use to calculate the plane-projected
        coordinates around.

    deg : bool
        If this is True, the input angles are assumed to be in degrees and the
        output is in degrees as well.

    Returns
    -------

    tuple of np.arrays
        This is the (`xi`, `eta`) coordinate pairs corresponding to the
        image-plane projected coordinates for each pair of input equatorial
        coordinates in (`inra`, `indecl`).

    '''

    if deg:

        ra = np.radians(inra)
        decl = np.radians(indecl)
        centerra = np.radians(incenterra)
        centerdecl = np.radians(incenterdecl)

    else:

        ra = inra
        decl = indecl
        centerra = incenterra
        centerdecl = incenterdecl

    cdecc = np.cos(centerdecl)
    sdecc = np.sin(centerdecl)
    crac = np.cos(centerra)
    srac = np.sin(centerra)

    uu = np.cos(decl)*np.cos(ra)
    vv = np.cos(decl)*np.sin(ra)
    ww = np.sin(decl)

    uun = uu*cdecc*crac + vv*cdecc*srac + ww*sdecc
    vvn = -uu*srac + vv*crac
    wwn = -uu*sdecc*crac - vv*sdecc*srac + ww*cdecc
    denom = vvn*vvn + wwn*wwn

    aunn = np.zeros_like(uun)
    aunn[uun >= 1.0] = 0.0
    aunn[uun < 1.0] = np.arccos(uun)

    xi, eta = np.zeros_like(aunn), np.zeros_like(aunn)

    xi[(aunn <= 0.0) | (denom <= 0.0)] = 0.0
    eta[(aunn <= 0.0) | (denom <= 0.0)] = 0.0

    sdenom = np.sqrt(denom)

    xi[(aunn > 0.0) | (denom > 0.0)] = aunn*vvn/sdenom
    eta[(aunn > 0.0) | (denom > 0.0)] = aunn*wwn/sdenom

    if deg:
        return np.degrees(xi), np.degrees(eta)
    else:
        return xi, eta