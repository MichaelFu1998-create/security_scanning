def get_update_tile(self, params, values):
        """ Get the amount of support size required for a particular update."""
        doglobal, particles = self._update_type(params)
        if doglobal:
            return self.shape.copy()

        # 1) store the current parameters of interest
        values0 = self.get_values(params)
        # 2) calculate the current tileset
        tiles0 = [self._tile(n) for n in particles]

        # 3) update to newer parameters and calculate tileset
        self.set_values(params, values)
        tiles1 = [self._tile(n) for n in particles]

        # 4) revert parameters & return union of all tiles
        self.set_values(params, values0)
        return Tile.boundingtile(tiles0 + tiles1)