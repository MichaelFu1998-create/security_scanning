def image_psf_shape_tag_from_image_psf_shape(image_psf_shape):
    """Generate an image psf shape tag, to customize phase names based on size of the image PSF that the original PSF \
    is trimmed to for faster run times.

    This changes the phase name 'phase_name' as follows:

    image_psf_shape = 1 -> phase_name
    image_psf_shape = 2 -> phase_name_image_psf_shape_2
    image_psf_shape = 2 -> phase_name_image_psf_shape_2
    """
    if image_psf_shape is None:
        return ''
    else:
        y = str(image_psf_shape[0])
        x = str(image_psf_shape[1])
        return ('_image_psf_' + y + 'x' + x)