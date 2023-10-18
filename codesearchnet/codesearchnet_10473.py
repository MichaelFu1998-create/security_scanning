def constant_regularization_matrix_from_pixel_neighbors(coefficients, pixel_neighbors, pixel_neighbors_size):
    """From the pixel-neighbors, setup the regularization matrix using the constant regularization scheme.

    Parameters
    ----------
    coefficients : tuple
        The regularization coefficients which controls the degree of smoothing of the inversion reconstruction.
    pixel_neighbors : ndarray
        An array of length (total_pixels) which provides the index of all neighbors of every pixel in \
        the Voronoi grid (entries of -1 correspond to no neighbor).
    pixel_neighbors_size : ndarrayy
        An array of length (total_pixels) which gives the number of neighbors of every pixel in the \
        Voronoi grid.
    """

    pixels = len(pixel_neighbors)

    regularization_matrix = np.zeros(shape=(pixels, pixels))

    regularization_coefficient = coefficients[0] ** 2.0

    for i in range(pixels):
        regularization_matrix[i, i] += 1e-8
        for j in range(pixel_neighbors_size[i]):
            neighbor_index = pixel_neighbors[i, j]
            regularization_matrix[i, i] += regularization_coefficient
            regularization_matrix[i, neighbor_index] -= regularization_coefficient

    return regularization_matrix