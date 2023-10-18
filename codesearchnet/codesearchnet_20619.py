def smooth_fwhm(self, fwhm):
        """ Set a smoothing Gaussian kernel given its FWHM in mm.  """
        if fwhm != self._smooth_fwhm:
            self._is_data_smooth = False
        self._smooth_fwhm = fwhm