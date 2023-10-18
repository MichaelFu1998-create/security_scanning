def mask_and_flatten(self):
        """Return a vector of the masked data.

        Returns
        -------
        np.ndarray, tuple of indices (np.ndarray), tuple of the mask shape
        """
        self._check_for_mask()

        return self.get_data(smoothed=True, masked=True, safe_copy=False)[self.get_mask_indices()],\
               self.get_mask_indices(), self.mask.shape