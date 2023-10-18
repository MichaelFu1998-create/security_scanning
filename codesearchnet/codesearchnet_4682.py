def euclidean_distance_square(point1, point2):
    """!
    @brief Calculate square Euclidean distance between two vectors.

    \f[
    dist(a, b) = \sum_{i=0}^{N}(a_{i} - b_{i})^{2};
    \f]

    @param[in] point1 (array_like): The first vector.
    @param[in] point2 (array_like): The second vector.

    @return (double) Square Euclidean distance between two vectors.

    @see euclidean_distance, manhattan_distance, chebyshev_distance

    """
    distance = 0.0
    for i in range(len(point1)):
        distance += (point1[i] - point2[i]) ** 2.0

    return distance