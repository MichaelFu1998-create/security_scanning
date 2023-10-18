def blurred_image_1d_from_1d_unblurred_and_blurring_images(unblurred_image_1d, blurring_image_1d, convolver):
    """For a 1D masked image and 1D blurring image (the regions outside the mask whose light blurs \
    into the mask after PSF convolution), use both to compute the blurred image within the mask via PSF convolution.

    The convolution uses each image's convolver (*See ccd.convolution*).

    Parameters
    ----------
    unblurred_image_1d : ndarray
        The 1D masked datas which is blurred.
    blurring_image_1d : ndarray
        The 1D masked blurring image which is used for blurring.
    convolver : ccd.convolution.ConvolverImage
        The image-convolver which performs the convolution in 1D.
    """
    return convolver.convolve_image(image_array=unblurred_image_1d, blurring_array=blurring_image_1d)