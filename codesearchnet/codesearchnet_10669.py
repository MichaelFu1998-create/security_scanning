def grid_angle_to_profile(self, grid_thetas):
        """The angle between each angle theta on the grid and the profile, in radians.

        Parameters
        -----------
        grid_thetas : ndarray
            The angle theta counter-clockwise from the positive x-axis to each coordinate in radians.
        """
        theta_coordinate_to_profile = np.add(grid_thetas, - self.phi_radians)
        return np.cos(theta_coordinate_to_profile), np.sin(theta_coordinate_to_profile)