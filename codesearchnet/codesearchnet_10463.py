def inversion_psf_shape_tag_from_inversion_psf_shape(inversion_psf_shape):
    """Generate an inversion psf shape tag, to customize phase names based on size of the inversion PSF that the \
    original PSF is trimmed to for faster run times.

    This changes the phase name 'phase_name' as follows:

    inversion_psf_shape = 1 -> phase_name
    inversion_psf_shape = 2 -> phase_name_inversion_psf_shape_2
    inversion_psf_shape = 2 -> phase_name_inversion_psf_shape_2
    """
    if inversion_psf_shape is None:
        return ''
    else:
        y = str(inversion_psf_shape[0])
        x = str(inversion_psf_shape[1])
        return ('_inv_psf_' + y + 'x' + x)