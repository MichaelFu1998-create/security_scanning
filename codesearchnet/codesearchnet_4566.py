def calculate_distance_matrix(sample):
    """!
    @brief Calculates distance matrix for data sample (sequence of points) using Euclidean distance as a metric.

    @param[in] sample (array_like): Data points that are used for distance calculation.

    @return (list) Matrix distance between data points.

    """

    amount_rows = len(sample);
    return [ [ euclidean_distance(sample[i], sample[j]) for j in range(amount_rows) ] for i in range(amount_rows) ];