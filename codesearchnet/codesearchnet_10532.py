def image_plane_pix_grid_from_regular_grid(self, regular_grid):
        """Calculate the image-plane pixelization from a regular-grid of coordinates (and its mask).

        See *grid_stacks.SparseToRegularGrid* for details on how this grid is calculated.

        Parameters
        -----------
        regular_grid : grids.RegularGrid
            The grid of (y,x) arc-second coordinates at the centre of every image value (e.g. image-pixels).
        """

        pixel_scale = regular_grid.mask.pixel_scale

        pixel_scales = ((regular_grid.masked_shape_arcsec[0] + pixel_scale) / (self.shape[0]),
                        (regular_grid.masked_shape_arcsec[1] + pixel_scale) / (self.shape[1]))

        return grids.SparseToRegularGrid(unmasked_sparse_grid_shape=self.shape, pixel_scales=pixel_scales,
                                         regular_grid=regular_grid, origin=regular_grid.mask.centre)