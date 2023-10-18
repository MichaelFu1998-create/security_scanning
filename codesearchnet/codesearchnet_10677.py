def voronoi_sub_to_pix_from_grids_and_geometry(sub_grid, regular_to_nearest_pix, sub_to_regular, pixel_centres,
                                               pixel_neighbors, pixel_neighbors_size):
    """ Compute the mappings between a set of sub-grid pixels and pixelization pixels, using information on \
    how the regular pixels hosting each sub-pixel map to their closest pixelization pixel on the image-plane pix-grid \
    and the pixelization's pixel centres.

    To determine the complete set of sub-pixel to pixelization pixel mappings, we must pair every sub-pixel to \
    its nearest pixel. Using a full nearest neighbor search to do this is slow, thus the pixel neighbors (derived via \
    the Voronoi grid) are used to localize each nearest neighbor search by using a graph search.

    Parameters
    ----------
    regular_grid : RegularGrid
        The grid of (y,x) arc-second coordinates at the centre of every unmasked pixel, which has been traced to \
        to an irregular grid via lens.
    regular_to_nearest_pix : ndarray
        A 1D array that maps every regular-grid pixel to its nearest pix-grid pixel (as determined on the unlensed \
        2D array).
    pixel_centres : (float, float)
        The (y,x) centre of every Voronoi pixel in arc-seconds.
    pixel_neighbors : ndarray
        An array of length (voronoi_pixels) which provides the index of all neighbors of every pixel in \
        the Voronoi grid (entries of -1 correspond to no neighbor).
    pixel_neighbors_size : ndarray
        An array of length (voronoi_pixels) which gives the number of neighbors of every pixel in the \
        Voronoi grid.
     """

    sub_to_pix = np.zeros((sub_grid.shape[0]))

    for sub_index in range(sub_grid.shape[0]):

        nearest_pix_pixel_index = regular_to_nearest_pix[sub_to_regular[sub_index]]

        while True:

            nearest_pix_pixel_center = pixel_centres[nearest_pix_pixel_index]

            sub_to_nearest_pix_distance = (sub_grid[sub_index, 0] - nearest_pix_pixel_center[0]) ** 2 + \
                                          (sub_grid[sub_index, 1] - nearest_pix_pixel_center[1]) ** 2

            closest_separation_from_pix_to_neighbor = 1.0e8

            for neighbor_index in range(pixel_neighbors_size[nearest_pix_pixel_index]):

                neighbor = pixel_neighbors[nearest_pix_pixel_index, neighbor_index]

                separation_from_neighbor = (sub_grid[sub_index, 0] - pixel_centres[neighbor, 0]) ** 2 + \
                                           (sub_grid[sub_index, 1] - pixel_centres[neighbor, 1]) ** 2

                if separation_from_neighbor < closest_separation_from_pix_to_neighbor:
                    closest_separation_from_pix_to_neighbor = separation_from_neighbor
                    closest_neighbor_index = neighbor_index

            neighboring_pix_pixel_index = pixel_neighbors[nearest_pix_pixel_index, closest_neighbor_index]
            sub_to_neighboring_pix_distance = closest_separation_from_pix_to_neighbor

            if sub_to_nearest_pix_distance <= sub_to_neighboring_pix_distance:
                sub_to_pix[sub_index] = nearest_pix_pixel_index
                break
            else:
                nearest_pix_pixel_index = neighboring_pix_pixel_index

    return sub_to_pix