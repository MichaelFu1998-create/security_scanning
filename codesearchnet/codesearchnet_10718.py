def curvature_matrix_from_blurred_mapping_matrix(blurred_mapping_matrix, noise_map_1d):
    """Compute the curvature matrix *F* from a blurred mapping matrix *f* and the 1D noise-map *\sigma* \
     (see Warren & Dye 2003).

    Parameters
    -----------
    blurred_mapping_matrix : ndarray
        The matrix representing the blurred mappings between sub-grid pixels and pixelization pixels.
    noise_map_1d : ndarray
        Flattened 1D array of the noise-map used by the inversion during the fit.
    """

    flist = np.zeros(blurred_mapping_matrix.shape[0])
    iflist = np.zeros(blurred_mapping_matrix.shape[0], dtype='int')
    return curvature_matrix_from_blurred_mapping_matrix_jit(blurred_mapping_matrix, noise_map_1d, flist, iflist)