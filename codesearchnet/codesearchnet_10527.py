def from_fits_renormalized(cls, file_path, hdu, pixel_scale):
        """Loads a PSF from fits and renormalizes it

        Parameters
        ----------
        pixel_scale
        file_path: String
            The path to the file containing the PSF
        hdu : int
            The HDU the PSF is stored in the .fits file.

        Returns
        -------
        psf: PSF
            A renormalized PSF instance
        """
        psf = PSF.from_fits_with_scale(file_path, hdu, pixel_scale)
        psf[:, :] = np.divide(psf, np.sum(psf))
        return psf