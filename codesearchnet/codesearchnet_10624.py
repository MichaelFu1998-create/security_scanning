def deflections_from_grid(self, grid, **kwargs):
        """
        Calculate the deflection angles at a given set of arc-second gridded coordinates.

        Parameters
        ----------
        grid : grids.RegularGrid
            The grid of (y,x) arc-second coordinates the deflection angles are computed on.
        """

        eta = np.multiply(1. / self.scale_radius, self.grid_to_grid_radii(grid))

        deflection_grid = np.multiply((4. * self.kappa_s * self.scale_radius / eta), self.deflection_func_sph(eta))

        return self.grid_to_grid_cartesian(grid, deflection_grid)