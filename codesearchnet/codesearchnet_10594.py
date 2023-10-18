def regular_to_sparse_from_sparse_mappings(regular_to_unmasked_sparse, unmasked_sparse_to_sparse):
    """Using the mapping between the regular-grid and unmasked pixelization grid, compute the mapping between each regular
    pixel and the masked pixelization grid.

    Parameters
    -----------
    regular_to_unmasked_sparse : ndarray
        The index mapping between every regular-pixel and masked pixelization pixel.
    unmasked_sparse_to_sparse : ndarray
        The index mapping between every masked pixelization pixel and unmasked pixelization pixel.
    """
    total_regular_pixels = regular_to_unmasked_sparse.shape[0]

    regular_to_sparse = np.zeros(total_regular_pixels)

    for regular_index in range(total_regular_pixels):
    #    print(regular_index, regular_to_unmasked_sparse[regular_index], unmasked_sparse_to_sparse.shape[0])
        regular_to_sparse[regular_index] = unmasked_sparse_to_sparse[regular_to_unmasked_sparse[regular_index]]


    return regular_to_sparse