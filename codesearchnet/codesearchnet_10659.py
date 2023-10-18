def voronoi_neighbors_from_pixels_and_ridge_points(pixels, ridge_points):
    """Compute the neighbors of every pixel as a list of the pixel index's each pixel shares a vertex with.

    The ridge points of the Voronoi grid are used to derive this.

    Parameters
    ----------
    ridge_points : scipy.spatial.Voronoi.ridge_points
        Each Voronoi-ridge (two indexes representing a pixel mapping_matrix).
    """

    pixel_neighbors_size = np.zeros(shape=(pixels))

    for ridge_index in range(ridge_points.shape[0]):
        pair0 = ridge_points[ridge_index, 0]
        pair1 = ridge_points[ridge_index, 1]
        pixel_neighbors_size[pair0] += 1
        pixel_neighbors_size[pair1] += 1

    pixel_neighbors_index = np.zeros(shape=(pixels))
    pixel_neighbors = -1 * np.ones(shape=(pixels, int(np.max(pixel_neighbors_size))))

    for ridge_index in range(ridge_points.shape[0]):
        pair0 = ridge_points[ridge_index, 0]
        pair1 = ridge_points[ridge_index, 1]
        pixel_neighbors[pair0, int(pixel_neighbors_index[pair0])] = pair1
        pixel_neighbors[pair1, int(pixel_neighbors_index[pair1])] = pair0
        pixel_neighbors_index[pair0] += 1
        pixel_neighbors_index[pair1] += 1

    return pixel_neighbors, pixel_neighbors_size