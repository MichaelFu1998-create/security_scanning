def minkowski_distance_numpy(object1, object2, degree=2):
    """!
    @brief Calculate Minkowski distance between objects using numpy.

    @param[in] object1 (array_like): The first array_like object.
    @param[in] object2 (array_like): The second array_like object.
    @param[in] degree (numeric): Degree of that is used for Minkowski distance.

    @return (double) Minkowski distance between two object.

    """
    return numpy.sum(numpy.power(numpy.power(object1 - object2, degree), 1/degree), axis=1).T