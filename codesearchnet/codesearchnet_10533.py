def geometry_from_grid(self, grid, buffer=1e-8):
        """Determine the geometry of the rectangular grid, by overlaying it over a grid of coordinates such that its \
         outer-most pixels align with the grid's outer most coordinates plus a small buffer.

        Parameters
        -----------
        grid : ndarray
            The (y,x) grid of coordinates over which the rectangular pixelization is placed to determine its geometry.
        buffer : float
            The size the pixelization is buffered relative to the grid.
        """
        y_min = np.min(grid[:, 0]) - buffer
        y_max = np.max(grid[:, 0]) + buffer
        x_min = np.min(grid[:, 1]) - buffer
        x_max = np.max(grid[:, 1]) + buffer
        pixel_scales = (float((y_max - y_min) / self.shape[0]), float((x_max - x_min) / self.shape[1]))
        origin = ((y_max + y_min) / 2.0, (x_max + x_min) / 2.0)
        pixel_neighbors, pixel_neighbors_size = self.neighbors_from_pixelization()
        return self.Geometry(shape=self.shape, pixel_scales=pixel_scales, origin=origin,
                             pixel_neighbors=pixel_neighbors, pixel_neighbors_size=pixel_neighbors_size)