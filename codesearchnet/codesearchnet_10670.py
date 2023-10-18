def rotate_grid_from_profile(self, grid_elliptical):
        """ Rotate a grid of elliptical (y,x) coordinates from the reference frame of the profile back to the \
        unrotated coordinate grid reference frame (coordinates are not shifted back to their original centre).

        This routine is used after computing deflection angles in the reference frame of the profile, so that the \
        deflection angles can be re-rotated to the frame of the original coordinates before performing ray-tracing.

        Parameters
        ----------
        grid_elliptical : TransformedGrid(ndarray)
            The (y, x) coordinates in the reference frame of an elliptical profile.
        """
        y = np.add(np.multiply(grid_elliptical[:, 1], self.sin_phi), np.multiply(grid_elliptical[:, 0], self.cos_phi))
        x = np.add(np.multiply(grid_elliptical[:, 1], self.cos_phi), - np.multiply(grid_elliptical[:, 0], self.sin_phi))
        return np.vstack((y, x)).T