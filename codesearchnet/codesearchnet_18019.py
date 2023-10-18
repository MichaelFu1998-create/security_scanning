def calc_particle_group_region_size(s, region_size=40, max_mem=1e9, **kwargs):
    """
    Finds the biggest region size for LM particle optimization with a
    given memory constraint.

    Input Parameters
    ----------------
        s : :class:`peri.states.ImageState`
            The state with the particles
        region_size : Int or 3-element list-like of ints, optional.
            The initial guess for the region size. Default is 40
        max_mem : Numeric, optional
            The maximum memory for the optimizer to take. Default is 1e9

    Other Parameters
    ----------------
        bounds: 2-element list-like of 3-element lists.
            The sub-region of the image over which to look for particles.
                bounds[0]: The lower-left  corner of the image region.
                bounds[1]: The upper-right corner of the image region.
            Default (None -> ([0,0,0], s.oshape.shape)) is a box of the entire
            image size, i.e. the default places every particle in the image
            somewhere in the groups.
    Returns
    -------
        region_size : numpy.ndarray of ints of the region size.
    """
    region_size = np.array(region_size).astype('int')

    def calc_mem_usage(region_size):
        rs = np.array(region_size)
        particle_groups = separate_particles_into_groups(s, region_size=
                rs.tolist(), **kwargs)
        # The actual mem usage is the max of the memory usage of all the
        # particle groups. However this is too slow. So instead we use the
        # max of the memory of the biggest 5 particle groups:
        numpart = [np.size(g) for g in particle_groups]
        biggroups = [particle_groups[i] for i in np.argsort(numpart)[-5:]]
        def get_tile_jsize(group):
            nms = s.param_particle(group)
            tile = s.get_update_io_tiles(nms, s.get_values(nms))[2]
            return tile.shape.prod() * len(nms)
        mems = [8*get_tile_jsize(g) for g in biggroups]  # 8 for bytes/float64
        return np.max(mems)

    im_shape = s.oshape.shape
    if calc_mem_usage(region_size) > max_mem:
        while ((calc_mem_usage(region_size) > max_mem) and
                np.any(region_size > 2)):
            region_size = np.clip(region_size-1, 2, im_shape)
    else:
        while ((calc_mem_usage(region_size) < max_mem) and
                np.any(region_size < im_shape)):
            region_size = np.clip(region_size+1, 2, im_shape)
        region_size -= 1 #need to be < memory, so we undo 1 iteration

    return region_size