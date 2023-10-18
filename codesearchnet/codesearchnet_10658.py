def rectangular_neighbors_from_shape(shape):
    """Compute the neighbors of every pixel as a list of the pixel index's each pixel shares a vertex with.

    The uniformity of the rectangular grid's geometry is used to compute this.
    """


    pixels = shape[0]*shape[1]

    pixel_neighbors = -1 * np.ones(shape=(pixels, 4))
    pixel_neighbors_size = np.zeros(pixels)

    pixel_neighbors, pixel_neighbors_size = compute_corner_neighbors(pixel_neighbors, pixel_neighbors_size,
                                                                     shape, pixels)
    pixel_neighbors, pixel_neighbors_size = compute_top_edge_neighbors(pixel_neighbors, pixel_neighbors_size,
                                                                       shape, pixels)
    pixel_neighbors, pixel_neighbors_size = compute_left_edge_neighbors(pixel_neighbors, pixel_neighbors_size,
                                                                        shape, pixels)
    pixel_neighbors, pixel_neighbors_size = compute_right_edge_neighbors(pixel_neighbors, pixel_neighbors_size,
                                                                         shape, pixels)
    pixel_neighbors, pixel_neighbors_size = compute_bottom_edge_neighbors(pixel_neighbors, pixel_neighbors_size,
                                                                          shape, pixels)
    pixel_neighbors, pixel_neighbors_size = compute_central_neighbors(pixel_neighbors, pixel_neighbors_size,
                                                                      shape, pixels)

    return pixel_neighbors, pixel_neighbors_size