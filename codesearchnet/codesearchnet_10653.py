def blurred_image_of_planes_from_1d_images_and_convolver(total_planes, image_plane_image_1d_of_planes,
                                                         image_plane_blurring_image_1d_of_planes, convolver,
                                                         map_to_scaled_array):
    """For a tracer, extract the image-plane image of every plane and blur it with the PSF.

    If none of the galaxies in a plane have a light profie or pixelization (and thus don't have an image) a *None* \
    is used.

    Parameters
    ----------
    total_planes : int
        The total number of planes that blurred images are computed for.
    image_plane_image_1d_of_planes : [ndarray]
        For every plane, the 1D image-plane image.
    image_plane_blurring_image_1d_of_planes : [ndarray]
        For every plane, the 1D image-plane blurring image.
    convolver : hyper.ccd.convolution.ConvolverImage
        Class which performs the PSF convolution of a masked image in 1D.
    map_to_scaled_array : func
        A function which maps a masked image from 1D to 2D.
    """

    blurred_image_of_planes = []

    for plane_index in range(total_planes):

        # If all entries are zero, there was no light profile / pixeization
        if np.count_nonzero(image_plane_image_1d_of_planes[plane_index]) > 0:

            blurred_image_1d_of_plane = blurred_image_1d_from_1d_unblurred_and_blurring_images(
                unblurred_image_1d=image_plane_image_1d_of_planes[plane_index],
                blurring_image_1d=image_plane_blurring_image_1d_of_planes[plane_index],
                convolver=convolver)

            blurred_image_of_plane = map_to_scaled_array(array_1d=blurred_image_1d_of_plane)

            blurred_image_of_planes.append(blurred_image_of_plane)

        else:

            blurred_image_of_planes.append(None)

    return blurred_image_of_planes