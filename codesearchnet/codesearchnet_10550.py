def new_grid_stack_with_pix_grid_added(self, pix_grid, regular_to_nearest_pix):
        """Setup a grid-stack of grid_stack using an existing grid-stack.
        
        The new grid-stack has the same grid_stack (regular, sub, blurring, etc.) as before, but adds a pix-grid as a \
        new attribute.

        Parameters
        -----------
        pix_grid : ndarray
            The grid of (y,x) arc-second coordinates of every image-plane pixelization grid used for adaptive \
             pixelizations.
        regular_to_nearest_pix : ndarray
            A 1D array that maps every regular-grid pixel to its nearest pix-grid pixel.
        """
        pix = PixGrid(arr=pix_grid, regular_to_nearest_pix=regular_to_nearest_pix)
        return GridStack(regular=self.regular, sub=self.sub, blurring=self.blurring, pix=pix)