def tile_overlap(inner, outer, norm=False):
    """ How much of inner is in outer by volume """
    div = 1.0/inner.volume if norm else 1.0
    return div*(inner.volume - util.Tile.intersection(inner, outer).volume)