def mapping_matrix_from_sub_to_pix(sub_to_pix, pixels, regular_pixels, sub_to_regular, sub_grid_fraction):
    """Computes the mapping matrix, by iterating over the known mappings between the sub-grid and pixelization.

    Parameters
    -----------
    sub_to_pix : ndarray
        The mappings between the observed regular's sub-pixels and pixelization's pixels.
    pixels : int
        The number of pixels in the pixelization.
    regular_pixels : int
        The number of datas pixels in the observed datas and thus on the regular grid.
    sub_to_regular : ndarray
        The mappings between the observed regular's sub-pixels and observed regular's pixels.
    sub_grid_fraction : float
        The fractional area each sub-pixel takes up in an regular-pixel.
    """

    mapping_matrix = np.zeros((regular_pixels, pixels))

    for sub_index in range(sub_to_regular.shape[0]):
        mapping_matrix[sub_to_regular[sub_index], sub_to_pix[sub_index]] += sub_grid_fraction

    return mapping_matrix