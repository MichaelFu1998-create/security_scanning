def mask_circular_annular_from_shape_pixel_scale_and_radii(shape, pixel_scale, inner_radius_arcsec, outer_radius_arcsec,
                                                           centre=(0.0, 0.0)):
    """Compute an annular masks from an input inner and outer masks radius and regular shape."""

    mask = np.full(shape, True)

    centres_arcsec = mask_centres_from_shape_pixel_scale_and_centre(shape=mask.shape, pixel_scale=pixel_scale, centre=centre)

    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):

            y_arcsec = (y - centres_arcsec[0]) * pixel_scale
            x_arcsec = (x - centres_arcsec[1]) * pixel_scale

            r_arcsec = np.sqrt(x_arcsec ** 2 + y_arcsec ** 2)

            if outer_radius_arcsec >= r_arcsec >= inner_radius_arcsec:
                mask[y, x] = False

    return mask