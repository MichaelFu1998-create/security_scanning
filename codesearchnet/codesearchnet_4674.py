def gaussian(data, mean, covariance):
    """!
    @brief Calculates gaussian for dataset using specified mean (mathematical expectation) and variance or covariance in case
            multi-dimensional data.
    
    @param[in] data (list): Data that is used for gaussian calculation.
    @param[in] mean (float|numpy.array): Mathematical expectation used for calculation.
    @param[in] covariance (float|numpy.array): Variance or covariance matrix for calculation.
    
    @return (list) Value of gaussian function for each point in dataset.
    
    """
    dimension = float(len(data[0]))
 
    if dimension != 1.0:
        inv_variance = numpy.linalg.pinv(covariance)
    else:
        inv_variance = 1.0 / covariance
    
    divider = (pi * 2.0) ** (dimension / 2.0) * numpy.sqrt(numpy.linalg.norm(covariance))
    if divider != 0.0:
        right_const = 1.0 / divider
    else:
        right_const = float('inf')
    
    result = []
    
    for point in data:
        mean_delta = point - mean
        point_gaussian = right_const * numpy.exp( -0.5 * mean_delta.dot(inv_variance).dot(numpy.transpose(mean_delta)) )
        result.append(point_gaussian)
    
    return result