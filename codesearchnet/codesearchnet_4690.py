def canberra_distance_numpy(object1, object2):
    """!
    @brief Calculate Canberra distance between two objects using numpy.

    @param[in] object1 (array_like): The first vector.
    @param[in] object2 (array_like): The second vector.

    @return (float) Canberra distance between two objects.

    """
    with numpy.errstate(divide='ignore', invalid='ignore'):
        result = numpy.divide(numpy.abs(object1 - object2), numpy.abs(object1) + numpy.abs(object2))

    if len(result.shape) > 1:
        return numpy.sum(numpy.nan_to_num(result), axis=1).T
    else:
        return numpy.sum(numpy.nan_to_num(result))