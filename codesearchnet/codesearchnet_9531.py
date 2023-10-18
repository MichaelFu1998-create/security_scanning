def read(self, **kwargs):
        """
        Read existing output data from a previous run.

        Returns
        -------
        process output : NumPy array (raster) or feature iterator (vector)
        """
        if self.tile.pixelbuffer > self.config.output.pixelbuffer:
            output_tiles = list(self.config.output_pyramid.tiles_from_bounds(
                self.tile.bounds, self.tile.zoom
            ))
        else:
            output_tiles = self.config.output_pyramid.intersecting(self.tile)
        return self.config.output.extract_subset(
            input_data_tiles=[
                (output_tile, self.config.output.read(output_tile))
                for output_tile in output_tiles
            ],
            out_tile=self.tile,
        )