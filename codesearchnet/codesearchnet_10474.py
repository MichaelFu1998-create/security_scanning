def weighted_pixel_signals_from_images(pixels, signal_scale, regular_to_pix, galaxy_image):
    """Compute the (scaled) signal in each pixel, where the signal is the sum of its datas_-pixel fluxes. \
    These pixel-signals are used to compute the effective regularization weight of each pixel.

    The pixel signals are scaled in the following ways:

    1) Divided by the number of datas_-pixels in the pixel, to ensure all pixels have the same \
    'relative' signal (i.e. a pixel with 10 regular-pixels doesn't have x2 the signal of one with 5).

    2) Divided by the maximum pixel-signal, so that all signals vary between 0 and 1. This ensures that the \
    regularizations weights are defined identically for any datas_ units or signal-to-noise_map ratio.

    3) Raised to the power of the hyper-parameter *signal_scale*, so the method can control the relative \
    contribution regularization in different regions of pixelization.

    Parameters
    -----------
    pixels : int
        The total number of pixels in the pixelization the regularization scheme is applied to.
    signal_scale : float
        A factor which controls how rapidly the smoothness of regularization varies from high signal regions to \
        low signal regions.
    regular_to_pix : ndarray
        A 1D array mapping every pixel on the regular-grid to a pixel on the pixelization.
    galaxy_image : ndarray
        The image of the galaxy which is used to compute the weigghted pixel signals.
    """

    pixel_signals = np.zeros((pixels,))
    pixel_sizes = np.zeros((pixels,))

    for regular_index in range(galaxy_image.shape[0]):
        pixel_signals[regular_to_pix[regular_index]] += galaxy_image[regular_index]
        pixel_sizes[regular_to_pix[regular_index]] += 1

    pixel_signals /= pixel_sizes
    pixel_signals /= np.max(pixel_signals)

    return pixel_signals ** signal_scale