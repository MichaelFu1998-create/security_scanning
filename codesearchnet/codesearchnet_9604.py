def to_dict(self):
        """
        Return dictionary representation of pyramid parameters.
        """
        return dict(
            grid=self.grid.to_dict(),
            metatiling=self.metatiling,
            tile_size=self.tile_size,
            pixelbuffer=self.pixelbuffer
        )