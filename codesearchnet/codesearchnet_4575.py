def average_inter_cluster_distance(cluster1, cluster2, data = None):
    """!
    @brief Calculates average inter-cluster distance between two clusters.
    @details Clusters can be represented by list of coordinates (in this case data shouldn't be specified),
             or by list of indexes of points from the data (represented by list of points), in this case 
             data should be specified.
             
    @param[in] cluster1 (list): The first cluster where each element can represent index from the data or object itself.
    @param[in] cluster2 (list): The second cluster where each element can represent index from the data or object itself.
    @param[in] data (list): If specified than elements of clusters will be used as indexes,
               otherwise elements of cluster will be considered as points.
    
    @return (double) Average inter-cluster distance between two clusters.
    
    """
    
    distance = 0.0;
    
    if (data is None):
        for i in range(len(cluster1)):
            for j in range(len(cluster2)):
                distance += euclidean_distance_square(cluster1[i], cluster2[j]);
    else:
        for i in range(len(cluster1)):
            for j in range(len(cluster2)):
                distance += euclidean_distance_square(data[ cluster1[i]], data[ cluster2[j]]);
    
    distance /= float(len(cluster1) * len(cluster2));
    return distance ** 0.5;