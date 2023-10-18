def mask_elliptical_from_shape_pixel_scale_and_radius(shape, pixel_scale, major_axis_radius_arcsec, axis_ratio, phi,
                                                      centre=(0.0, 0.0)):
    """Compute a circular masks from an input masks radius and regular shape."""

    mask = np.full(shape, True)

    centres_arcsec = mask_centres_from_shape_pixel_scale_and_centre(shape=mask.shape, pixel_scale=pixel_scale,
                                                                  centre=centre)

    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):

            y_arcsec = (y - centres_arcsec[0]) * pixel_scale
            x_arcsec = (x - centres_arcsec[1]) * pixel_scale

            r_arcsec_elliptical = elliptical_radius_from_y_x_phi_and_axis_ratio(y_arcsec, x_arcsec, phi, axis_ratio)

            if r_arcsec_elliptical <= major_axis_radius_arcsec:
                mask[y, x] = False

    return mask