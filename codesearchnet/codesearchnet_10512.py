def load_psf(psf_path, psf_hdu, pixel_scale, renormalize=False):
    """Factory for loading the psf from a .fits file.

    Parameters
    ----------
    psf_path : str
        The path to the psf .fits file containing the psf (e.g. '/path/to/psf.fits')
    psf_hdu : int
        The hdu the psf is contained in the .fits file specified by *psf_path*.
    pixel_scale : float
        The size of each pixel in arc seconds.
    renormalize : bool
        If True, the PSF is renoralized such that all elements sum to 1.0.
    """
    if renormalize:
        return PSF.from_fits_renormalized(file_path=psf_path, hdu=psf_hdu, pixel_scale=pixel_scale)
    if not renormalize:
        return PSF.from_fits_with_scale(file_path=psf_path, hdu=psf_hdu, pixel_scale=pixel_scale)