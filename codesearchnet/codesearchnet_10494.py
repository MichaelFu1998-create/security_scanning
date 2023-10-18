def regular_to_pix(self):
        """The 1D index mappings between the regular pixels and Voronoi pixelization pixels."""
        return mapper_util.voronoi_regular_to_pix_from_grids_and_geometry(regular_grid=self.grid_stack.regular,
               regular_to_nearest_pix=self.grid_stack.pix.regular_to_nearest_pix,
               pixel_centres=self.geometry.pixel_centres, pixel_neighbors=self.geometry.pixel_neighbors,
               pixel_neighbors_size=self.geometry.pixel_neighbors_size).astype('int')