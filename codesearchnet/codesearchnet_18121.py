def locate_spheres(image, feature_rad, dofilter=False, order=(3 ,3, 3),
                    trim_edge=True, **kwargs):
    """
    Get an initial featuring of sphere positions in an image.

    Parameters
    -----------
    image : :class:`peri.util.Image` object
        Image object which defines the image file as well as the region.

    feature_rad : float
        Radius of objects to find, in pixels. This is a featuring radius
        and not a real radius, so a better value is frequently smaller
        than the real radius (half the actual radius is good). If ``use_tp``
        is True, then the twice ``feature_rad`` is passed as trackpy's
        ``diameter`` keyword.

    dofilter : boolean, optional
        Whether to remove the background before featuring. Doing so can
        often greatly increase the success of initial featuring and
        decrease later optimization time. Filtering functions by fitting
        the image to a low-order polynomial and featuring the residuals.
        In doing so, this will change the mean intensity of the featured
        image and hence the good value of ``minmass`` will change when
        ``dofilter`` is True. Default is False.

    order : 3-element tuple, optional
        If `dofilter`, the 2+1D Leg Poly approximation to the background
        illumination field. Default is (3,3,3).

    Other Parameters
    ----------------
    invert : boolean, optional
        Whether to invert the image for featuring. Set to True if the
        image is dark particles on a bright background. Default is True
    minmass : Float or None, optional
        The minimum mass/masscut of a particle. Default is None, which
        calculates internally.
    use_tp : Bool, optional
        Whether or not to use trackpy. Default is False, since trackpy
        cuts out particles at the edge.

    Returns
    --------
    positions : np.ndarray [N,3]
        Positions of the particles in order (z,y,x) in image pixel units.

    Notes
    -----
    Optionally filters the image by fitting the image I(x,y,z) to a
    polynomial, then subtracts this fitted intensity variation and uses
    centroid methods to find the particles.
    """
    # We just want a smoothed field model of the image so that the residuals
    # are simply the particles without other complications
    m = models.SmoothFieldModel()
    I = ilms.LegendrePoly2P1D(order=order, constval=image.get_image().mean())
    s = states.ImageState(image, [I], pad=0, mdl=m)
    if dofilter:
        opt.do_levmarq(s, s.params)
    pos = addsub.feature_guess(s, feature_rad, trim_edge=trim_edge, **kwargs)[0]
    return pos