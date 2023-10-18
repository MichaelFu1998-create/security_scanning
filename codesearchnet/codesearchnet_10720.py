def reconstructed_data_vector_from_blurred_mapping_matrix_and_solution_vector(blurred_mapping_matrix, solution_vector):
    """ Compute the reconstructed hyper vector from the blurrred mapping matrix *f* and solution vector *S*.

    Parameters
    -----------
    blurred_mapping_matrix : ndarray
        The matrix representing the blurred mappings between sub-grid pixels and pixelization pixels.

    """
    reconstructed_data_vector = np.zeros(blurred_mapping_matrix.shape[0])
    for i in range(blurred_mapping_matrix.shape[0]):
        for j in range(solution_vector.shape[0]):
            reconstructed_data_vector[i] += solution_vector[j] * blurred_mapping_matrix[i, j]

    return reconstructed_data_vector