def get_data(self, smoothed=True, masked=True, safe_copy=False):
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
        if not safe_copy and smoothed == self._is_data_smooth and masked == self._is_data_masked:
            if self.has_data_loaded() and self._caching == 'fill':
                return self.get_data()

        if safe_copy:
            data = get_data(self.img)
        else:
            data = self.img.get_data(caching=self._caching)

        is_smoothed = False
        if smoothed and self._smooth_fwhm > 0:
            try:
                data = _smooth_data_array(data, self.get_affine(), self._smooth_fwhm, copy=False)
            except ValueError as ve:
                raise ValueError('Error smoothing image {} with a {}mm FWHM '
                                 'kernel.'.format(self.img, self._smooth_fwhm)) from ve
            else:
                is_smoothed = True

        is_data_masked = False
        if masked and self.has_mask():
            try:
                data = self.unmask(self._mask_data(data)[0])
            except:
                raise
            else:
                is_data_masked = True

        if not safe_copy:
            self._is_data_masked = is_data_masked
            self._is_data_smooth = is_smoothed

        return data