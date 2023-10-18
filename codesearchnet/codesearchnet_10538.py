def mapper_from_grid_stack_and_border(self, grid_stack, border):
        """Setup a Voronoi mapper from an adaptive-magnification pixelization, as follows:

        1) (before this routine is called), setup the 'pix' grid as part of the grid-stack, which corresponds to a \
           sparse set of pixels in the image-plane which are traced to form the pixel centres.
        2) If a border is supplied, relocate all of the grid-stack's regular, sub and pix grid pixels beyond the border.
        3) Determine the adaptive-magnification pixelization's pixel centres, by extracting them from the relocated \
           pix grid.
        4) Use these pixelization centres to setup the Voronoi pixelization.
        5) Determine the neighbors of every Voronoi cell in the Voronoi pixelization.
        6) Setup the geometry of the pixelizatioon using the relocated sub-grid and Voronoi pixelization.
        7) Setup a Voronoi mapper from all of the above quantities.

        Parameters
        ----------
        grid_stack : grids.GridStack
            A collection of grid describing the observed image's pixel coordinates (includes an image and sub grid).
        border : grids.RegularGridBorder
            The borders of the grid_stacks (defined by their image-plane masks).
        """

        if border is not None:
            relocated_grids = border.relocated_grid_stack_from_grid_stack(grid_stack)
        else:
            relocated_grids = grid_stack

        pixel_centres = relocated_grids.pix
        pixels = pixel_centres.shape[0]

        voronoi = self.voronoi_from_pixel_centers(pixel_centres)

        pixel_neighbors, pixel_neighbors_size = self.neighbors_from_pixelization(pixels=pixels,
                                                                                 ridge_points=voronoi.ridge_points)
        geometry = self.geometry_from_grid(grid=relocated_grids.sub, pixel_centres=pixel_centres,
                                           pixel_neighbors=pixel_neighbors,
                                           pixel_neighbors_size=pixel_neighbors_size)

        return mappers.VoronoiMapper(pixels=pixels, grid_stack=relocated_grids, border=border,
                                     voronoi=voronoi, geometry=geometry)