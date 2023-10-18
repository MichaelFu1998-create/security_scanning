def unmasked_blurred_image_of_planes_and_galaxies_from_padded_grid_stack_and_psf(planes, padded_grid_stack, psf):
    """For lens data, compute the unmasked blurred image of every unmasked unblurred image of every galaxy in each \
    plane. To do this, this function iterates over all planes and then galaxies to extract their unmasked unblurred \
    images.

    If a galaxy in a plane has a pixelization, the unmasked image of that galaxy in the plane is returned as None \
    as as the inversion's model image cannot be mapped to an unmasked version.

    This relies on using the lens data's padded-grid, which is a grid of (y,x) coordinates which extends over the \
    entire image as opposed to just the masked region.

    This returns a list of lists, where each list index corresponds to [plane_index][galaxy_index].

    Parameters
    ----------
    planes : [plane.Plane]
        The list of planes the unmasked blurred images are computed using.
    padded_grid_stack : grids.GridStack
        A padded-grid_stack, whose padded grid is used for PSF convolution.
    psf : ccd.PSF
        The PSF of the image used for convolution.
    """
    return [plane.unmasked_blurred_image_of_galaxies_from_psf(padded_grid_stack, psf) for plane in planes]