def closest_uniform_tile(s, shift, size, other):
    """
    Given a tiling of space (by state, shift, and size), find the closest
    tile to another external tile
    """
    region = util.Tile(size, dim=s.dim, dtype='float').translate(shift - s.pad)
    vec = np.round((other.center - region.center) / region.shape)
    return region.translate(region.shape * vec)