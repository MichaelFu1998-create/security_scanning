def masked_sub_grid_1d_index_to_2d_sub_pixel_index_from_mask(mask, sub_grid_size):
    """Compute a 1D array that maps every unmasked pixel to its corresponding 2d pixel using its (y,x) pixel indexes.

    For howtolens if pixel [2,5] corresponds to the second pixel on the 1D array, grid_to_pixel[1] = [2,5]"""

    total_sub_pixels = total_sub_pixels_from_mask_and_sub_grid_size(mask=mask, sub_grid_size=sub_grid_size)
    sub_grid_to_sub_pixel = np.zeros(shape=(total_sub_pixels, 2))
    sub_pixel_count = 0

    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            if not mask[y, x]:
                for y1 in range(sub_grid_size):
                    for x1 in range(sub_grid_size):
                        sub_grid_to_sub_pixel[sub_pixel_count, :] = (y*sub_grid_size)+y1, (x*sub_grid_size)+x1
                        sub_pixel_count += 1

    return sub_grid_to_sub_pixel