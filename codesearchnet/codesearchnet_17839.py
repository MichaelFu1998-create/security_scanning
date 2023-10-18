def identify_misfeatured_regions(st, filter_size=5, sigma_cutoff=8.):
    """
    Identifies regions of missing/misfeatured particles based on the
    residuals' local deviation from uniform Gaussian noise.

    Parameters
    ----------
    st : :class:`peri.states.State`
        The state in which to identify mis-featured regions.

    filter_size : Int, best if odd.
        The size of the filter for calculating the local standard deviation;
        should approximately be the size of a poorly featured region in
        each dimension. Default is 5.

    sigma_cutoff : Float or `otsu`, optional
        The max allowed deviation of the residuals from what is expected,
        in units of the residuals' standard deviation. Lower means more
        sensitive, higher = less sensitive. Default is 8.0, i.e. one pixel
        out of every 7*10^11 is mis-identified randomly. In practice the
        noise is not Gaussian so there are still some regions mis-identified
        as improperly featured. Set to ```otsu``` to calculate this number
        based on an automatic Otsu threshold.

    Returns
    -------
    tiles : List of :class:`peri.util.Tile`
        Each tile is the smallest bounding tile that contains an improperly
        featured region. The list is sorted by the tile's volume.

    Notes
    -----
    Algorithm is
    1.  Create a field of the local standard deviation, as measured over
        a hypercube of size filter_size.
    2.  Find the maximum reasonable value of the field. [The field should
        be a random variable with mean of r.std() and standard deviation
        of ~r.std() / sqrt(N), where r is the residuals and N is the
        number of pixels in the hypercube.]
    3.  Label & Identify the misfeatured regions as portions where
        the local error is too large.
    4.  Parse the misfeatured regions into tiles.
    5.  Return the sorted tiles.
    The Otsu option to calculate the sigma cutoff works well for images
    that actually contain missing particles, returning a number similar
    to one calculated with a sigma cutoff. However, if the image is
    well-featured with Gaussian residuals, then the Otsu threshold
    splits the Gaussian down the middle instead of at the tails, which
    is very bad. So use with caution.
    """
    # 1. Field of local std
    r = st.residuals
    weights = np.ones([filter_size]*len(r.shape), dtype='float')
    weights /= weights.sum()
    f = np.sqrt(nd.filters.convolve(r*r, weights, mode='reflect'))

    # 2. Maximal reasonable value of the field.
    if sigma_cutoff == 'otsu':
        max_ok = initializers.otsu_threshold(f)
    else:
        # max_ok = f.mean() * (1 + sigma_cutoff / np.sqrt(weights.size))
        max_ok = f.mean() + sigma_cutoff * f.std()

    # 3. Label & Identify
    bad = f > max_ok
    labels, n = nd.measurements.label(bad)
    inds = []
    for i in range(1, n+1):
        inds.append(np.nonzero(labels == i))

    # 4. Parse into tiles
    tiles = [Tile(np.min(ind, axis=1), np.max(ind, axis=1)+1) for ind in inds]

    # 5. Sort and return
    volumes = [t.volume for t in tiles]
    return [tiles[i] for i in np.argsort(volumes)[::-1]]