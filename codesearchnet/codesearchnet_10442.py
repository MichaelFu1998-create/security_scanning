def total_sparse_pixels_from_mask(mask, unmasked_sparse_grid_pixel_centres):
    """Given the full (i.e. without removing pixels which are outside the regular-masks) pixelization grid's pixel centers
    and the regular-masks, compute the total number of pixels which are within the regular-masks and thus used by the
    pixelization grid.

    Parameters
    -----------
    mask : ccd.masks.Mask
        The regular-masks within which pixelization pixels must be inside
    unmasked_sparse_grid_pixel_centres : ndarray
        The centres of the unmasked pixelization grid pixels.
    """

    total_sparse_pixels = 0

    for unmasked_sparse_pixel_index in range(unmasked_sparse_grid_pixel_centres.shape[0]):

        y = unmasked_sparse_grid_pixel_centres[unmasked_sparse_pixel_index, 0]
        x = unmasked_sparse_grid_pixel_centres[unmasked_sparse_pixel_index, 1]

        if not mask[y,x]:
            total_sparse_pixels += 1

    return total_sparse_pixels