def intensities_of_galaxies_from_grid(grid, galaxies):
    """Compute the intensities of a list of galaxies from an input grid, by summing the individual intensities \
    of each galaxy's light profile.

    If the input grid is a *grids.SubGrid*, the intensites is calculated on the sub-grid and binned-up to the \
    original regular grid by taking the mean value of every set of sub-pixels.

    If no galaxies are entered into the function, an array of all zeros is returned.

    Parameters
    -----------
    grid : RegularGrid
        The grid (regular or sub) of (y,x) arc-second coordinates at the centre of every unmasked pixel which the \
        intensities are calculated on.
    galaxies : [galaxy.Galaxy]
        The galaxies whose light profiles are used to compute the surface densities.
    """
    if galaxies:
        return sum(map(lambda g: g.intensities_from_grid(grid), galaxies))
    else:
        return np.full((grid.shape[0]), 0.0)