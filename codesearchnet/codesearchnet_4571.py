def average_neighbor_distance(points, num_neigh):
    """!
    @brief Returns average distance for establish links between specified number of nearest neighbors.
    
    @param[in] points (list): Input data, list of points where each point represented by list.
    @param[in] num_neigh (uint): Number of neighbors that should be used for distance calculation.
    
    @return (double) Average distance for establish links between 'num_neigh' in data set 'points'.
    
    """
    
    if num_neigh > len(points) - 1:
        raise NameError('Impossible to calculate average distance to neighbors when number of object is less than number of neighbors.');
    
    dist_matrix = [ [ 0.0 for i in range(len(points)) ] for j in range(len(points)) ];
    for i in range(0, len(points), 1):
        for j in range(i + 1, len(points), 1):
            distance = euclidean_distance(points[i], points[j]);
            dist_matrix[i][j] = distance;
            dist_matrix[j][i] = distance;
            
        dist_matrix[i] = sorted(dist_matrix[i]);

    total_distance = 0;
    for i in range(0, len(points), 1):
        # start from 0 - first element is distance to itself.
        for j in range(0, num_neigh, 1):
            total_distance += dist_matrix[i][j + 1];
            
    return ( total_distance / (num_neigh * len(points)) );