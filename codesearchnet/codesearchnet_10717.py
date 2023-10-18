def data_vector_from_blurred_mapping_matrix_and_data(blurred_mapping_matrix, image_1d, noise_map_1d):
    """Compute the hyper vector *D* from a blurred mapping matrix *f* and the 1D image *d* and 1D noise-map *\sigma* \
    (see Warren & Dye 2003).
    
    Parameters
    -----------
    blurred_mapping_matrix : ndarray
        The matrix representing the blurred mappings between sub-grid pixels and pixelization pixels.
    image_1d : ndarray
        Flattened 1D array of the observed image the inversion is fitting.
    noise_map_1d : ndarray
        Flattened 1D array of the noise-map used by the inversion during the fit.
    """

    mapping_shape = blurred_mapping_matrix.shape

    data_vector = np.zeros(mapping_shape[1])

    for image_index in range(mapping_shape[0]):
        for pix_index in range(mapping_shape[1]):
            data_vector[pix_index] += image_1d[image_index] * \
                                      blurred_mapping_matrix[image_index, pix_index] / (noise_map_1d[image_index] ** 2.0)

    return data_vector