def deflections_of_galaxies_from_sub_grid(sub_grid, galaxies):
    """Compute the deflections of a list of galaxies from an input sub-grid, by summing the individual deflections \
    of each galaxy's mass profile.

    The deflections are calculated on the sub-grid and binned-up to the original regular grid by taking the mean value \
    of every set of sub-pixels.

    If no galaxies are entered into the function, an array of all zeros is returned.

    Parameters
    -----------
    sub_grid : RegularGrid
        The grid (regular or sub) of (y,x) arc-second coordinates at the centre of every unmasked pixel which the \
        deflections is calculated on.
    galaxies : [galaxy.Galaxy]
        The galaxies whose mass profiles are used to compute the surface densities.
    """
    if galaxies:
        return sum(map(lambda galaxy: galaxy.deflections_from_grid(sub_grid), galaxies))
    else:
        return np.full((sub_grid.shape[0], 2), 0.0)