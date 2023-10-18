def deflections_from_grid(self, grid):
        """
        Calculate the deflection angles at a given set of arc-second gridded coordinates.

        Parameters
        ----------
        grid : grids.RegularGrid
            The grid of (y,x) arc-second coordinates the deflection angles are computed on.
        """

        def calculate_deflection_component(npow, index):
            deflection_grid = self.axis_ratio * grid[:, index]
            deflection_grid *= quad_grid(self.deflection_func, 0.0, 1.0, grid,
                                         args=(npow, self.axis_ratio, self.kappa_s,
                                               self.scale_radius))[0]

            return deflection_grid

        deflection_y = calculate_deflection_component(1.0, 0)
        deflection_x = calculate_deflection_component(0.0, 1)

        return self.rotate_grid_from_profile(np.multiply(1.0, np.vstack((deflection_y, deflection_x)).T))