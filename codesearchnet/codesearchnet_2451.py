def _create_vec_field(fval, gradf, d1x, d2x, color_axis, smooth=0):
    """Calculate the deformation vector field
    In:
    fval: float
    gradf: numpy.ndarray
        of shape C x h x w with C = 3 or C = 1
        (color channels), h, w >= 1.
    d1x: numpy.ndarray
        of shape C x h x w and [type] = 'Float' or 'Double'.
    d2x: numpy.ndarray
        of shape C x h x w and [type] = 'Float' or 'Double'.
    smooth: float
        Width of the Gaussian kernel used for smoothing
        (default is 0 for no smoothing).
    Out:
    vec_field: numpy.ndarray
        of shape (2, h, w).
    """

    if color_axis == 2:
        gradf = _transpose_image(gradf)

    c, h, w = gradf.shape  # colors, height, width

    # Sum over color channels
    alpha1 = np.sum(gradf * d1x, axis=0)
    alpha2 = np.sum(gradf * d2x, axis=0)

    norm_squared_alpha = (alpha1 ** 2).sum() + (alpha2 ** 2).sum()

    # Smoothing
    if smooth > 0:
        alpha1 = gaussian_filter(alpha1, smooth)
        alpha2 = gaussian_filter(alpha2, smooth)
        norm_squared_alpha = (alpha1 ** 2).sum() + (alpha2 ** 2).sum()
        # In theory, we need to apply the filter a second time.
        alpha1 = gaussian_filter(alpha1, smooth)
        alpha2 = gaussian_filter(alpha2, smooth)

    vec_field = np.empty((h, w, 2))
    vec_field[:, :, 0] = -fval * alpha1 / norm_squared_alpha
    vec_field[:, :, 1] = -fval * alpha2 / norm_squared_alpha

    return vec_field