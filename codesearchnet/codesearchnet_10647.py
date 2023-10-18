def convergence_of_galaxies_from_grid(grid, galaxies):
    """Compute the convergence of a list of galaxies from an input grid, by summing the individual convergence \
    of each galaxy's mass profile.

    If the input grid is a *grids.SubGrid*, the convergence is calculated on the sub-grid and binned-up to the \
    original regular grid by taking the mean value of every set of sub-pixels.

    If no galaxies are entered into the function, an array of all zeros is returned.

    Parameters
    -----------
    grid : RegularGrid
        The grid (regular or sub) of (y,x) arc-second coordinates at the centre of every unmasked pixel which the \
        convergence is calculated on.
    galaxies : [galaxy.Galaxy]
        The galaxies whose mass profiles are used to compute the convergence.
    """
    if galaxies:
        return sum(map(lambda g: g.convergence_from_grid(grid), galaxies))
    else:
        return np.full((grid.shape[0]), 0.0)