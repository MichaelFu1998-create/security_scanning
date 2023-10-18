def relocated_grid_stack_from_grid_stack(self, grid_stack):
        """Determine a set of relocated grid_stack from an input set of grid_stack, by relocating their pixels based on the \
        borders.

        The blurring-grid does not have its coordinates relocated, as it is only used for computing analytic \
        light-profiles and not inversion-grid_stack.

        Parameters
        -----------
        grid_stack : GridStack
            The grid-stack, whose grid_stack coordinates are relocated.
        """
        border_grid = grid_stack.regular[self]
        return GridStack(regular=self.relocated_grid_from_grid_jit(grid=grid_stack.regular, border_grid=border_grid),
                         sub=self.relocated_grid_from_grid_jit(grid=grid_stack.sub, border_grid=border_grid),
                         blurring=None,
                         pix=self.relocated_grid_from_grid_jit(grid=grid_stack.pix, border_grid=border_grid))