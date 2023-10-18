def deflections_of_galaxies_from_grid(grid, galaxies):
    """Compute the deflections of a list of galaxies from an input grid, by summing the individual deflections \
    of each galaxy's mass profile.

    If the input grid is a *grids.SubGrid*, the potential is calculated on the sub-grid and binned-up to the \
    original regular grid by taking the mean value of every set of sub-pixels.

    If no galaxies are entered into the function, an array of all zeros is returned.

    Parameters
    -----------
    grid : RegularGrid
        The grid (regular or sub) of (y,x) arc-second coordinates at the centre of every unmasked pixel which the \
        deflections is calculated on.
    galaxies : [galaxy.Galaxy]
        The galaxies whose mass profiles are used to compute the surface densities.
    """
    if len(galaxies) > 0:
        deflections = sum(map(lambda galaxy: galaxy.deflections_from_grid(grid), galaxies))
    else:
        deflections = np.full((grid.shape[0], 2), 0.0)

    if isinstance(grid, grids.SubGrid):
        return np.asarray([grid.regular_data_1d_from_sub_data_1d(deflections[:, 0]),
                           grid.regular_data_1d_from_sub_data_1d(deflections[:, 1])]).T

    return deflections