def separate_particles_into_groups(s, region_size=40, bounds=None,
        doshift=False):
    """
    Separates particles into convenient groups for optimization.

    Given a state, returns a list of groups of particles. Each group of
    particles are located near each other in the image. Every particle
    located in the desired region is contained in exactly 1 group.

    Parameters
    ----------
    s : :class:`peri.states.ImageState`
        The peri state to find particles in.
    region_size : Int or 3-element list-like of ints, optional
        The size of the box. Groups particles into boxes of shape
        (region_size[0], region_size[1], region_size[2]). If region_size
        is a scalar, the box is a cube of length region_size.
        Default is 40.
    bounds : 2-element list-like of 3-element lists, optional
        The sub-region of the image over which to look for particles.
            bounds[0]: The lower-left  corner of the image region.
            bounds[1]: The upper-right corner of the image region.
        Default (None -> ([0,0,0], s.oshape.shape)) is a box of the entire
        image size, i.e. the default places every particle in the image
        somewhere in the groups.
    doshift : {True, False, `'rand'`}, optional
        Whether or not to shift the tile boxes by half a region size, to
        prevent the same particles to be chosen every time. If `'rand'`,
        randomly chooses either True or False. Default is False

    Returns
    -------
    particle_groups : List
        Each element of particle_groups is an int numpy.ndarray of the
        group of nearby particles. Only contains groups with a nonzero
        number of particles, so the elements don't necessarily correspond
        to a given image region.
    """
    imtile = s.oshape.translate(-s.pad)
    bounding_tile = (imtile if bounds is None else Tile(bounds[0], bounds[1]))
    rs = (np.ones(bounding_tile.dim, dtype='int')*region_size if
            np.size(region_size) == 1 else np.array(region_size))

    n_translate = np.ceil(bounding_tile.shape.astype('float')/rs).astype('int')
    particle_groups = []
    tile = Tile(left=bounding_tile.l, right=bounding_tile.l + rs)
    if doshift == 'rand':
        doshift = np.random.choice([True, False])
    if doshift:
        shift = rs // 2
        n_translate += 1
    else:
        shift = 0
    deltas = np.meshgrid(*[np.arange(i) for i in n_translate])
    positions = s.obj_get_positions()
    if bounds is None:
        # FIXME this (deliberately) masks a problem where optimization
        # places particles outside the image. However, it ensures that
        # all particles are in at least one group when `bounds is None`,
        # which is the use case within opt. The 1e-3 is to ensure that
        # they are inside the box and not on the edge.
        positions = np.clip(positions, imtile.l+1e-3, imtile.r-1e-3)
    groups = list(map(lambda *args: find_particles_in_tile(positions,
            tile.translate( np.array(args) * rs - shift)), *[d.ravel()
            for d in deltas]))

    for i in range(len(groups)-1, -1, -1):
        if groups[i].size == 0:
            groups.pop(i)
    assert _check_groups(s, groups)
    return groups