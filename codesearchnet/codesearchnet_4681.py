def euclidean_distance_numpy(object1, object2):
    """!
    @brief Calculate Euclidean distance between two objects using numpy.

    @param[in] object1 (array_like): The first array_like object.
    @param[in] object2 (array_like): The second array_like object.

    @return (double) Euclidean distance between two objects.

    """
    return numpy.sum(numpy.sqrt(numpy.square(object1 - object2)), axis=1).T