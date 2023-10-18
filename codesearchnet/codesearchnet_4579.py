def data_corners(data, data_filter = None):
    """!
    @brief Finds maximum and minimum corner in each dimension of the specified data.
    
    @param[in] data (list): List of points that should be analysed.
    @param[in] data_filter (list): List of indexes of the data that should be analysed,
                if it is 'None' then whole 'data' is analysed to obtain corners.
    
    @return (list) Tuple of two points that corresponds to minimum and maximum corner (min_corner, max_corner).
    
    """
    
    dimensions = len(data[0])
    
    bypass = data_filter
    if bypass is None:
        bypass = range(len(data))
    
    maximum_corner = list(data[bypass[0]][:])
    minimum_corner = list(data[bypass[0]][:])
    
    for index_point in bypass:
        for index_dimension in range(dimensions):
            if data[index_point][index_dimension] > maximum_corner[index_dimension]:
                maximum_corner[index_dimension] = data[index_point][index_dimension]
            
            if data[index_point][index_dimension] < minimum_corner[index_dimension]:
                minimum_corner[index_dimension] = data[index_point][index_dimension]
    
    return minimum_corner, maximum_corner