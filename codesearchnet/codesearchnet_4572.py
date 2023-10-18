def medoid(data, indexes=None, **kwargs):
    """!
    @brief Calculate medoid for input points using Euclidean distance.
    
    @param[in] data (list): Set of points for that median should be calculated.
    @param[in] indexes (list): Indexes of input set of points that will be taken into account during median calculation.
    @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'metric', 'data_type').

    <b>Keyword Args:</b><br>
        - metric (distance_metric): Metric that is used for distance calculation between two points.
        - data_type (string): Data type of input sample 'data' (available values: 'points', 'distance_matrix').

    @return (uint) index of point in input set that corresponds to median.
    
    """
    
    index_median = None
    distance = float('Inf')

    metric = kwargs.get('metric', type_metric.EUCLIDEAN_SQUARE)
    data_type = kwargs.get('data_type', 'points')

    if data_type == 'points':
        calculator = lambda index1, index2: metric(data[index1], data[index2])
    elif data_type == 'distance_matrix':
        if isinstance(data, numpy.matrix):
            calculator = lambda index1, index2: data.item(index1, index2)

        else:
            calculator = lambda index1, index2: data[index1][index2]
    else:
        raise TypeError("Unknown type of data is specified '%s'." % data_type)

    if indexes is None:
        range_points = range(len(data))
    else:
        range_points = indexes
    
    for index_candidate in range_points:
        distance_candidate = 0.0
        for index in range_points:
            distance_candidate += calculator(index_candidate, index)
        
        if distance_candidate < distance:
            distance = distance_candidate
            index_median = index_candidate
    
    return index_median