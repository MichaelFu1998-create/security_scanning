def curvature_matrix_from_blurred_mapping_matrix_jit(blurred_mapping_matrix, noise_map_1d, flist, iflist):
    """Compute the curvature matrix *F* from a blurred mapping matrix *f* and the 1D noise-map *\sigma* \
    (see Warren & Dye 2003).

    Parameters
    -----------
    blurred_mapping_matrix : ndarray
        The matrix representing the blurred mappings between sub-grid pixels and pixelization pixels.
    noise_map_1d : ndarray
        Flattened 1D array of the noise-map used by the inversion during the fit.
    flist : ndarray
        NumPy array of floats used to store mappings for efficienctly calculation.
    iflist : ndarray
        NumPy array of integers used to store mappings for efficienctly calculation.
    """
    curvature_matrix = np.zeros((blurred_mapping_matrix.shape[1], blurred_mapping_matrix.shape[1]))

    for image_index in range(blurred_mapping_matrix.shape[0]):
        index = 0
        for pixel_index in range(blurred_mapping_matrix.shape[1]):
            if blurred_mapping_matrix[image_index, pixel_index] > 0.0:
                flist[index] = blurred_mapping_matrix[image_index, pixel_index] / noise_map_1d[image_index]
                iflist[index] = pixel_index
                index += 1

        if index > 0:
            for i1 in range(index):
                for j1 in range(index):
                    ix = iflist[i1]
                    iy = iflist[j1]
                    curvature_matrix[ix, iy] += flist[i1] * flist[j1]

    for i in range(blurred_mapping_matrix.shape[1]):
        for j in range(blurred_mapping_matrix.shape[1]):
            curvature_matrix[i, j] = curvature_matrix[j, i]

    return curvature_matrix