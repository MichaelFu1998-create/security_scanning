def from_shape_pixel_scale_and_sub_grid_size(cls, shape, pixel_scale, sub_grid_size=2):
        """Setup a grid-stack of grid_stack from a 2D array shape, a pixel scale and a sub-grid size.
        
        This grid corresponds to a fully unmasked 2D array.

        Parameters
        -----------
        shape : (int, int)
            The 2D shape of the array, where all pixels are used to generate the grid-stack's grid_stack.
        pixel_scale : float
            The size of each pixel in arc seconds.            
        sub_grid_size : int
            The size of a sub-pixel's sub-grid (sub_grid_size x sub_grid_size).
        """
        regular_grid = RegularGrid.from_shape_and_pixel_scale(shape=shape, pixel_scale=pixel_scale)
        sub_grid = SubGrid.from_shape_pixel_scale_and_sub_grid_size(shape=shape, pixel_scale=pixel_scale,
                                                                    sub_grid_size=sub_grid_size)
        blurring_grid = np.array([[0.0, 0.0]])
        return GridStack(regular_grid, sub_grid, blurring_grid)