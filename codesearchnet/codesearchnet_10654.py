def unmasked_blurred_image_of_planes_from_padded_grid_stack_and_psf(planes, padded_grid_stack, psf):
    """For lens data, compute the unmasked blurred image of every unmasked unblurred image of each plane. To do this, \
    this function iterates over all planes to extract their unmasked unblurred images.

    If a galaxy in a plane has a pixelization, the unmasked image is returned as None, as as the inversion's model \
    image cannot be mapped to an unmasked version.

    This relies on using the lens data's padded-grid, which is a grid of (y,x) coordinates which extends over the \
    entire image as opposed to just the masked region.

    This returns a list, where each list index corresponds to [plane_index].

    Parameters
    ----------
    planes : [plane.Plane]
        The list of planes the unmasked blurred images are computed using.
    padded_grid_stack : grids.GridStack
        A padded-grid_stack, whose padded grid is used for PSF convolution.
    psf : ccd.PSF
        The PSF of the image used for convolution.
    """
    unmasked_blurred_image_of_planes = []

    for plane in planes:

        if plane.has_pixelization:
            unmasked_blurred_image_of_plane = None
        else:
            unmasked_blurred_image_of_plane = \
                padded_grid_stack.unmasked_blurred_image_from_psf_and_unmasked_image(

                    psf=psf, unmasked_image_1d=plane.image_plane_image_1d)

        unmasked_blurred_image_of_planes.append(unmasked_blurred_image_of_plane)

    return unmasked_blurred_image_of_planes