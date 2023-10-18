def sub_to_pix(self):
        """  The 1D index mappings between the sub pixels and Voronoi pixelization pixels. """
        return mapper_util.voronoi_sub_to_pix_from_grids_and_geometry(sub_grid=self.grid_stack.sub,
               regular_to_nearest_pix=self.grid_stack.pix.regular_to_nearest_pix,
               sub_to_regular=self.grid_stack.sub.sub_to_regular, pixel_centres=self.geometry.pixel_centres,
               pixel_neighbors=self.geometry.pixel_neighbors,
               pixel_neighbors_size=self.geometry.pixel_neighbors_size).astype('int')