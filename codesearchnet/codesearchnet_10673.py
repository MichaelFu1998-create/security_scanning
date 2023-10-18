def transform_grid_to_reference_frame(self, grid):
        """Transform a grid of (y,x) coordinates to the reference frame of the profile, including a translation to \
        its centre and a rotation to it orientation.

        Parameters
        ----------
        grid : ndarray
            The (y, x) coordinates in the original reference frame of the grid.
        """
        if self.__class__.__name__.startswith("Spherical"):
            return super().transform_grid_to_reference_frame(grid)
        shifted_coordinates = np.subtract(grid, self.centre)
        radius = np.sqrt(np.sum(shifted_coordinates ** 2.0, 1))
        theta_coordinate_to_profile = np.arctan2(shifted_coordinates[:, 0],
                                                 shifted_coordinates[:, 1]) - self.phi_radians
        transformed = np.vstack(
            (radius * np.sin(theta_coordinate_to_profile), radius * np.cos(theta_coordinate_to_profile))).T
        return transformed.view(TransformedGrid)