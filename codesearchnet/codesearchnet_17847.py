def separate_particles_into_groups(s, region_size=40, bounds=None):
    """
    Given a state, returns a list of groups of particles. Each group of
    particles are located near each other in the image. Every particle
    located in the desired region is contained in exactly 1 group.

    Parameters:
    -----------
    s : state
        The PERI state to find particles in.

    region_size: int or list of ints
        The size of the box. Groups particles into boxes of shape region_size.
        If region_size is a scalar, the box is a cube of length region_size.
        Default is 40.

    bounds: 2-element list-like of 3-element lists.
        The sub-region of the image over which to look for particles.
            bounds[0]: The lower-left  corner of the image region.
            bounds[1]: The upper-right corner of the image region.
        Default (None -> ([0,0,0], s.oshape.shape)) is a box of the entire
        image size, i.e. the default places every particle in the image
        somewhere in the groups.

    Returns:
    -----------
    particle_groups: list
        Each element of particle_groups is an int numpy.ndarray of the
        group of nearby particles. Only contains groups with a nonzero
        number of particles, so the elements don't necessarily correspond
        to a given image region.
    """
    imtile = (
        s.oshape.translate(-s.pad) if bounds is None else
        util.Tile(bounds[0], bounds[1])
    )

    # does all particle including out of image, is that correct?
    region = util.Tile(region_size, dim=s.dim)
    trange = np.ceil(imtile.shape.astype('float') / region.shape)

    translations = util.Tile(trange).coords(form='vector')
    translations = translations.reshape(-1, translations.shape[-1])

    groups = []
    positions = s.obj_get_positions()
    for v in translations:
        tmptile = region.copy().translate(region.shape * v - s.pad)
        groups.append(find_particles_in_tile(positions, tmptile))

    return [g for g in groups if len(g) > 0]