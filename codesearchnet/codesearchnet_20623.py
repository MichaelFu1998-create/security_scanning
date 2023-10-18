def _mask_data(self, data):
        """Return the data masked with self.mask

        Parameters
        ----------
        data: np.ndarray

        Returns
        -------
        masked np.ndarray

        Raises
        ------
        ValueError if the data and mask dimensions are not compatible.
        Other exceptions related to numpy computations.
        """
        self._check_for_mask()

        msk_data = self.mask.get_data()
        if self.ndim == 3:
            return data[msk_data], np.where(msk_data)
        elif self.ndim == 4:
            return _apply_mask_to_4d_data(data, self.mask)
        else:
            raise ValueError('Cannot mask {} with {} dimensions using mask {}.'.format(self, self.ndim, self.mask))