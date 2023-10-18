def calculate_ellipse_description(covariance, scale = 2.0):
    """!
    @brief Calculates description of ellipse using covariance matrix.
    
    @param[in] covariance (numpy.array): Covariance matrix for which ellipse area should be calculated.
    @param[in] scale (float): Scale of the ellipse.
    
    @return (float, float, float) Return ellipse description: angle, width, height.
    
    """
    
    eigh_values, eigh_vectors = numpy.linalg.eigh(covariance)
    order = eigh_values.argsort()[::-1]
    
    values, vectors = eigh_values[order], eigh_vectors[order]
    angle = numpy.degrees(numpy.arctan2(*vectors[:,0][::-1]))

    if 0.0 in values:
        return 0, 0, 0

    width, height = 2.0 * scale * numpy.sqrt(values)
    return angle, width, height