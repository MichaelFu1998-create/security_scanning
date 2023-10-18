def total_regular_pixels_from_mask(mask):
    """Compute the total number of unmasked regular pixels in a masks."""

    total_regular_pixels = 0

    for y in range(mask.shape[0]):
        for x in range(mask.shape[1]):
            if not mask[y, x]:
                total_regular_pixels += 1

    return total_regular_pixels