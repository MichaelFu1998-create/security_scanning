def total_border_pixels_from_mask_and_edge_pixels(mask, edge_pixels, masked_grid_index_to_pixel):
    """Compute the total number of borders-pixels in a masks."""

    border_pixel_total = 0

    for i in range(edge_pixels.shape[0]):

        if check_if_border_pixel(mask, edge_pixels[i], masked_grid_index_to_pixel):
            border_pixel_total += 1

    return border_pixel_total