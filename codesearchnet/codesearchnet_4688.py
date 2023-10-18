def minkowski_distance(point1, point2, degree=2):
    """!
    @brief Calculate Minkowski distance between two vectors.

    \f[
    dist(a, b) = \sqrt[p]{ \sum_{i=0}^{N}\left(a_{i} - b_{i}\right)^{p} };
    \f]

    @param[in] point1 (array_like): The first vector.
    @param[in] point2 (array_like): The second vector.
    @param[in] degree (numeric): Degree of that is used for Minkowski distance.

    @return (double) Minkowski distance between two vectors.

    @see euclidean_distance

    """
    distance = 0.0
    for i in range(len(point1)):
        distance += (point1[i] - point2[i]) ** degree

    return distance ** (1.0 / degree)