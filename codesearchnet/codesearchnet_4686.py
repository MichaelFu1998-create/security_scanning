def chebyshev_distance(point1, point2):
    """!
    @brief Calculate Chebyshev distance between between two vectors.

    \f[
    dist(a, b) = \max_{}i\left (\left | a_{i} - b_{i} \right |\right );
    \f]

    @param[in] point1 (array_like): The first vector.
    @param[in] point2 (array_like): The second vector.

    @return (double) Chebyshev distance between two vectors.

    @see euclidean_distance_square, euclidean_distance, minkowski_distance

    """
    distance = 0.0
    dimension = len(point1)

    for i in range(dimension):
        distance = max(distance, abs(point1[i] - point2[i]))

    return distance