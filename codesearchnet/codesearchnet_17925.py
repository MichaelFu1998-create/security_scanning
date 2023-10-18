def local_max_featuring(im, radius=2.5, noise_size=1., bkg_size=None,
        minmass=1., trim_edge=False):
    """Local max featuring to identify bright spherical particles on a
    dark background.

    Parameters
    ----------
        im : numpy.ndarray
            The image to identify particles in.
        radius : Float > 0, optional
            Featuring radius of the particles. Default is 2.5
        noise_size : Float, optional
            Size of Gaussian kernel for smoothing out noise. Default is 1.
        bkg_size : Float or None, optional
            Size of the Gaussian kernel for removing long-wavelength
            background. Default is None, which gives `2 * radius`
        minmass : Float, optional
            Return only particles with a ``mass > minmass``. Default is 1.
        trim_edge : Bool, optional
            Set to True to omit particles identified exactly at the edge
            of the image. False-positive features frequently occur here
            because of the reflected bandpass featuring. Default is
            False, i.e. find particles at the edge of the image.

    Returns
    -------
        pos, mass : numpy.ndarray
            Particle positions and masses
    """
    if radius <= 0:
        raise ValueError('`radius` must be > 0')
    #1. Remove noise
    filtered = nd.gaussian_filter(im, noise_size, mode='mirror')
    #2. Remove long-wavelength background:
    if bkg_size is None:
        bkg_size = 2*radius
    filtered -= nd.gaussian_filter(filtered, bkg_size, mode='mirror')
    #3. Local max feature
    footprint = generate_sphere(radius)
    e = nd.maximum_filter(filtered, footprint=footprint)
    mass_im = nd.convolve(filtered, footprint, mode='mirror')
    good_im = (e==filtered) * (mass_im > minmass)
    pos = np.transpose(np.nonzero(good_im))
    if trim_edge:
        good = np.all(pos > 0, axis=1) & np.all(pos+1 < im.shape, axis=1)
        pos = pos[good, :].copy()
    masses = mass_im[pos[:,0], pos[:,1], pos[:,2]].copy()
    return pos, masses