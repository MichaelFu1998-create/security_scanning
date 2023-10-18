def border_pixels_from_mask(mask):
    """Compute a 1D array listing all borders pixel indexes in the masks. A borders pixel is a pixel which:

     1) is not fully surrounding by False masks values.
     2) Can reach the edge of the array without hitting a masked pixel in one of four directions (upwards, downwards,
     left, right).

     The borders pixels are thus pixels which are on the exterior edge of the masks. For example, the inner ring of edge \
     pixels in an annular masks are edge pixels but not borders pixels."""

    edge_pixels = edge_pixels_from_mask(mask)
    masked_grid_index_to_pixel = masked_grid_1d_index_to_2d_pixel_index_from_mask(mask)

    border_pixel_total = total_border_pixels_from_mask_and_edge_pixels(mask, edge_pixels, masked_grid_index_to_pixel)

    border_pixels = np.zeros(border_pixel_total)

    border_pixel_index = 0

    for edge_pixel_index in range(edge_pixels.shape[0]):

        if check_if_border_pixel(mask, edge_pixels[edge_pixel_index], masked_grid_index_to_pixel):
            border_pixels[border_pixel_index] = edge_pixels[edge_pixel_index]
            border_pixel_index += 1

    return border_pixels