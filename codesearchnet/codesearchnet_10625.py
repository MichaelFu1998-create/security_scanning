def potential_from_grid(self, grid):
        """
        Calculate the potential at a given set of arc-second gridded coordinates.

        Parameters
        ----------
        grid : grids.RegularGrid
            The grid of (y,x) arc-second coordinates the deflection angles are computed on.
        """
        potential_grid = quad_grid(self.potential_func, 0.0, 1.0, grid,
                                   args=(self.axis_ratio, self.kappa_s, self.scale_radius),
                                   epsrel=1.49e-5)[0]

        return potential_grid