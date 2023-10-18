def convert_PSFLab_xz(data, x_step=0.5, z_step=0.5, normalize=False):
    """Process a 2D array (from PSFLab .mat file) containing a x-z PSF slice.

    The input data is the raw array saved by PSFLab. The returned array has
    the x axis cut in half (only positive x) to take advantage of the
    rotational symmetry around z. Pysical dimensions (`x_step` and `z_step)
    are also assigned.

    If `nomalize` is True the peak is normalized to 1.

    Returns:
    x, z: (1D array) the X and Z axis in pysical units
    hdata: (2D array) the PSF intesity
    izm: (float) the index of PSF max along z (axis 0) for x=0 (axis 1)
    """
    z_len, x_len = data.shape
    hdata = data[:, (x_len - 1) // 2:]
    x = np.arange(hdata.shape[1]) * x_step
    z = np.arange(-(z_len - 1) / 2, (z_len - 1) / 2 + 1) * z_step
    if normalize:
        hdata /= hdata.max()  # normalize to 1 at peak
    return x, z, hdata, hdata[:, 0].argmax()