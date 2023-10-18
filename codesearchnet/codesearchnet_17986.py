def reflect_overhang(self, clip):
        """
        Compute the overhang and reflect it internally so respect periodic
        padding rules (see states._tile_from_particle_change). Returns both
        the inner tile and the inner tile with necessary pad.
        """
        orig = self.copy()
        tile = self.copy()

        hangl, hangr = tile.overhang(clip)
        tile = tile.pad(hangl)
        tile = tile.pad(hangr)

        inner = Tile.intersection([clip, orig])
        outer = Tile.intersection([clip, tile])
        return inner, outer