def find_particles_in_tile(positions, tile):
    """
    Finds the particles in a tile, as numpy.ndarray of ints.

    Parameters
    ----------
        positions : `numpy.ndarray`
            [N,3] array of the particle positions to check in the tile
        tile : :class:`peri.util.Tile` instance
            Tile of the region inside which to check for particles.

    Returns
    -------
        numpy.ndarray, int
            The indices of the particles in the tile.
    """
    bools = tile.contains(positions)
    return np.arange(bools.size)[bools]