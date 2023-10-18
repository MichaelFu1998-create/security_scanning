def manhattan_distance(a, b):
    """!
    @brief Calculate Manhattan distance between vector a and b.
    
    @param[in] a (list): The first cluster.
    @param[in] b (list): The second cluster.
    
    @return (double) Manhattan distance between two vectors.
    
    """
    
    if ( ((type(a) == float) and (type(b) == float)) or ((type(a) == int) and (type(b) == int)) ):
        return abs(a - b);
    
    distance = 0.0;
    dimension = len(a);
    
    for i in range(0, dimension):
        distance += abs(a[i] - b[i]);
    
    return distance;