def chebyshev_distance_numpy(object1, object2):
    """!
    @brief Calculate Chebyshev distance between two objects using numpy.

    @param[in] object1 (array_like): The first array_like object.
    @param[in] object2 (array_like): The second array_like object.

    @return (double) Chebyshev distance between two objects.

    """
    return numpy.max(numpy.absolute(object1 - object2), axis=1).T