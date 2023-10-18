def weighted_regularization_matrix_from_pixel_neighbors(regularization_weights, pixel_neighbors,
                                                        pixel_neighbors_size):
    """From the pixel-neighbors, setup the regularization matrix using the weighted regularization scheme.

    Parameters
    ----------
    regularization_weights : ndarray
        The regularization_ weight of each pixel, which governs how much smoothing is applied to that individual pixel.
    pixel_neighbors : ndarray
        An array of length (total_pixels) which provides the index of all neighbors of every pixel in \
        the Voronoi grid (entries of -1 correspond to no neighbor).
    pixel_neighbors_size : ndarrayy
        An array of length (total_pixels) which gives the number of neighbors of every pixel in the \
        Voronoi grid.
    """

    pixels = len(regularization_weights)

    regularization_matrix = np.zeros(shape=(pixels, pixels))

    regularization_weight = regularization_weights ** 2.0

    for i in range(pixels):
        for j in range(pixel_neighbors_size[i]):
            neighbor_index = pixel_neighbors[i, j]
            regularization_matrix[i, i] += regularization_weight[neighbor_index]
            regularization_matrix[neighbor_index, neighbor_index] += regularization_weight[neighbor_index]
            regularization_matrix[i, neighbor_index] -= regularization_weight[neighbor_index]
            regularization_matrix[neighbor_index, i] -= regularization_weight[neighbor_index]

    return regularization_matrix