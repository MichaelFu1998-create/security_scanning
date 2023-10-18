def mapper_from_grid_stack_and_border(self, grid_stack, border):
        """Setup a rectangular mapper from a rectangular pixelization, as follows:

        1) If a border is supplied, relocate all of the grid-stack's regular and sub grid pixels beyond the border.
        2) Determine the rectangular pixelization's geometry, by laying the pixelization over the sub-grid.
        3) Setup the rectangular mapper from the relocated grid-stack and rectangular pixelization.

        Parameters
        ----------
        grid_stack : grids.GridStack
            A stack of grid describing the observed image's pixel coordinates (e.g. an image-grid, sub-grid, etc.).
        border : grids.RegularGridBorder | None
            The border of the grid-stack's regular-grid.
        """

        if border is not None:
            relocated_grid_stack = border.relocated_grid_stack_from_grid_stack(grid_stack)
        else:
            relocated_grid_stack = grid_stack

        geometry = self.geometry_from_grid(grid=relocated_grid_stack.sub)

        return mappers.RectangularMapper(pixels=self.pixels, grid_stack=relocated_grid_stack, border=border,
                                         shape=self.shape, geometry=geometry)