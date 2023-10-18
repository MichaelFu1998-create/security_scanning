def regular_data_1d_from_sub_data_1d(self, sub_array_1d):
        """For an input sub-gridded array, map its hyper-values from the sub-gridded values to a 1D regular grid of \
        values by summing each set of each set of sub-pixels values and dividing by the total number of sub-pixels.

        Parameters
        -----------
        sub_array_1d : ndarray
            A 1D sub-gridded array of values (e.g. the intensities, surface-densities, potential) which is mapped to
            a 1d regular array.
        """
        return np.multiply(self.sub_grid_fraction, sub_array_1d.reshape(-1, self.sub_grid_length).sum(axis=1))