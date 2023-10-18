def manhattan_distance(point1, point2):
    """!
    @brief Calculate Manhattan distance between between two vectors.

    \f[
    dist(a, b) = \sum_{i=0}^{N}\left | a_{i} - b_{i} \right |;
    \f]

    @param[in] point1 (array_like): The first vector.
    @param[in] point2 (array_like): The second vector.

    @return (double) Manhattan distance between two vectors.

    @see euclidean_distance_square, euclidean_distance, chebyshev_distance

    """
    distance = 0.0
    dimension = len(point1)

    for i in range(dimension):
        distance += abs(point1[i] - point2[i])

    return distance