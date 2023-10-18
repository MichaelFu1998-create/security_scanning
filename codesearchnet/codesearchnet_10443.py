def mask_circular_from_shape_pixel_scale_and_radius(shape, pixel_scale, radius_arcsec, centre=(0.0, 0.0)):
    """Compute a circular masks from an input masks radius and regular shape."""

    mask = np.full(shape, True)

    centres_arcsec = mask_centres_from_shape_pixel_scale_and_centre(shape=mask.shape, pixel_scale=pixel_scale, centre=centre)

    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):

            y_arcsec = (y - centres_arcsec[0]) * pixel_scale
            x_arcsec = (x - centres_arcsec[1]) * pixel_scale

            r_arcsec = np.sqrt(x_arcsec ** 2 + y_arcsec ** 2)

            if r_arcsec <= radius_arcsec:
                mask[y, x] = False

    return mask