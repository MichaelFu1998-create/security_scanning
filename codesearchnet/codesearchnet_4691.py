def chi_square_distance(point1, point2):
    """!
    @brief Calculate Chi square distance between two vectors.

    \f[
    dist(a, b) = \sum_{i=0}^{N}\frac{\left ( a_{i} - b_{i} \right )^{2}}{\left | a_{i} \right | + \left | b_{i} \right |};
    \f]

    @param[in] point1 (array_like): The first vector.
    @param[in] point2 (array_like): The second vector.

    @return (float) Chi square distance between two objects.

    """
    distance = 0.0
    for i in range(len(point1)):
        divider = abs(point1[i]) + abs(point2[i])
        if divider == 0.0:
            continue

        distance += ((point1[i] - point2[i]) ** 2.0) / divider

    return distance