def _smooth_img(nii_img, smooth_fwhm):
        """
        Parameters
        ----------
        nii_img: nipy.Image

        smooth_fwhm: float

        Returns
        -------
        smoothed nipy.Image
        """
        # delayed import because could not install nipy on Python 3 on OSX
        from   nipy.algorithms.kernel_smooth import LinearFilter

        if smooth_fwhm <= 0:
            return nii_img

        filter = LinearFilter(nii_img.coordmap, nii_img.shape)
        return filter.smooth(nii_img)