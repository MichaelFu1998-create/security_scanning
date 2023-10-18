def _compose(image, vec_field, color_axis):
    """Calculate the composition of the function image with the vector
    field vec_field by interpolation.
    new_func = compose(image, vec_field)
    In:
    image: numpy.ndarray
        of shape C x h x w with C = 3 or C = 1 (color channels),
        h, w >= 2, and [type] = 'Float' or 'Double'.
        Contains the values of a function f: R ^ 2 -> R ^ C
        on the grid {0, ..., h - 1} x {0, ..., w - 1}.
    vec_field: numpy.array
        of shape (h, w, 2)
    vec_field[y, x, 0] is the x-coordinate of the vector vec_field[y, x]
    vec_field[y, x, 1] is the y-coordinate of the vector vec_field[y, x]
    positive x-direction is along rows from left to right
    positive y-direction is along columns from above to below
    """

    if color_axis == 2:
        image = _transpose_image(image)

    c, h, w = image.shape  # colors, height, width
    hrange = np.arange(h)
    wrange = np.arange(w)
    MGx, MGy = np.meshgrid(wrange, hrange)

    defMGx = (MGx + vec_field[:, :, 0]).clip(0, w - 1)
    defMGy = (MGy + vec_field[:, :, 1]).clip(0, h - 1)

    new_image = np.empty_like(image)

    for channel in range(c):
        # Get a linear interpolation for this color channel.
        interpolation = RectBivariateSpline(hrange, wrange, image[channel],
                                            kx=1, ky=1)

        # grid = False since the deformed grid is irregular
        new_image[channel] = interpolation(defMGy, defMGx, grid=False)
    if color_axis == 2:
        return _re_transpose_image(new_image)
    else:
        return new_image