def apply_smoothing(self, smooth_fwhm):
        """Set self._smooth_fwhm and then smooths the data.
        See boyle.nifti.smooth.smooth_imgs.

        Returns
        -------
        the smoothed data deepcopied.

        """
        if smooth_fwhm <= 0:
            return

        old_smooth_fwhm   = self._smooth_fwhm
        self._smooth_fwhm = smooth_fwhm
        try:
            data = self.get_data(smoothed=True, masked=True, safe_copy=True)
        except ValueError as ve:
            self._smooth_fwhm = old_smooth_fwhm
            raise
        else:
            self._smooth_fwhm = smooth_fwhm
            return data