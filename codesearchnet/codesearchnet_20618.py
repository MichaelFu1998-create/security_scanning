def get_data(self, safe_copy=False):
        """Get the data in the image.
         If save_copy is True, will perform a deep copy of the data and return it.

        Parameters
        ----------
        smoothed: (optional) bool
            If True and self._smooth_fwhm > 0 will smooth the data before masking.

        masked: (optional) bool
            If True and self.has_mask will return the masked data, the plain data otherwise.

        safe_copy: (optional) bool

        Returns
        -------
        np.ndarray
        """
        if safe_copy:
            data = get_data(self.img)
        else:
            data = self.img.get_data(caching=self._caching)

        return data