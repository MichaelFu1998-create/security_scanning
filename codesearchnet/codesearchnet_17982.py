def intersection(tiles, *args):
        """
        Intersection of tiles, returned as a tile

        >>> Tile.intersection(Tile([0, 1], [5, 4]), Tile([1, 0], [4, 5]))
        Tile [1, 1] -> [4, 4] ([3, 3])
        """
        tiles = listify(tiles) + listify(args)

        if len(tiles) < 2:
            return tiles[0]

        tile = tiles[0]
        l, r = tile.l.copy(), tile.r.copy()
        for tile in tiles[1:]:
            l = amax(l, tile.l)
            r = amin(r, tile.r)
        return Tile(l, r, dtype=l.dtype)