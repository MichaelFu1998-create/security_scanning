def geometry_from_grid(self, grid, pixel_centres, pixel_neighbors, pixel_neighbors_size, buffer=1e-8):
        """Determine the geometry of the Voronoi pixelization, by alligning it with the outer-most coordinates on a \
        grid plus a small buffer.

        Parameters
        -----------
        grid : ndarray
            The (y,x) grid of coordinates which determine the Voronoi pixelization's geometry.
        pixel_centres : ndarray
            The (y,x) centre of every Voronoi pixel in arc-seconds.
        origin : (float, float)
            The arc-second origin of the Voronoi pixelization's coordinate system.
        pixel_neighbors : ndarray
            An array of length (voronoi_pixels) which provides the index of all neighbors of every pixel in \
            the Voronoi grid (entries of -1 correspond to no neighbor).
        pixel_neighbors_size : ndarrayy
            An array of length (voronoi_pixels) which gives the number of neighbors of every pixel in the \
            Voronoi grid.
        """
        y_min = np.min(grid[:, 0]) - buffer
        y_max = np.max(grid[:, 0]) + buffer
        x_min = np.min(grid[:, 1]) - buffer
        x_max = np.max(grid[:, 1]) + buffer
        shape_arcsec = (y_max - y_min, x_max - x_min)
        origin = ((y_max + y_min) / 2.0, (x_max + x_min) / 2.0)
        return self.Geometry(shape_arcsec=shape_arcsec, pixel_centres=pixel_centres, origin=origin,
                             pixel_neighbors=pixel_neighbors, pixel_neighbors_size=pixel_neighbors_size)