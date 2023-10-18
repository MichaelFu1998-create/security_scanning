def sparse_grid_from_unmasked_sparse_grid(unmasked_sparse_grid, sparse_to_unmasked_sparse):
    """Use the central arc-second coordinate of every unmasked pixelization grid's pixels and mapping between each
    pixelization pixel and unmasked pixelization pixel to compute the central arc-second coordinate of every masked
    pixelization grid pixel.

    Parameters
    -----------
    unmasked_sparse_grid : ndarray
        The (y,x) arc-second centre of every unmasked pixelization grid pixel.
    sparse_to_unmasked_sparse : ndarray
        The index mapping between every pixelization pixel and masked pixelization pixel.
    """
    total_pix_pixels = sparse_to_unmasked_sparse.shape[0]

    pix_grid = np.zeros((total_pix_pixels, 2))

    for pixel_index in range(total_pix_pixels):
        pix_grid[pixel_index, 0] = unmasked_sparse_grid[sparse_to_unmasked_sparse[pixel_index], 0]
        pix_grid[pixel_index, 1] = unmasked_sparse_grid[sparse_to_unmasked_sparse[pixel_index], 1]

    return pix_grid