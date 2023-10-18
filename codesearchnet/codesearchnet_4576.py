def average_intra_cluster_distance(cluster1, cluster2, data=None):
    """!
    @brief Calculates average intra-cluster distance between two clusters.
    @details Clusters can be represented by list of coordinates (in this case data shouldn't be specified),
             or by list of indexes of points from the data (represented by list of points), in this case 
             data should be specified.
    
    @param[in] cluster1 (list): The first cluster.
    @param[in] cluster2 (list): The second cluster.
    @param[in] data (list): If specified than elements of clusters will be used as indexes,
               otherwise elements of cluster will be considered as points.
    
    @return (double) Average intra-cluster distance between two clusters.
    
    """
        
    distance = 0.0
    
    for i in range(len(cluster1) + len(cluster2)):
        for j in range(len(cluster1) + len(cluster2)):
            if data is None:
                # the first point
                if i < len(cluster1):
                    first_point = cluster1[i]
                else:
                    first_point = cluster2[i - len(cluster1)]
                
                # the second point
                if j < len(cluster1):
                    second_point = cluster1[j]
                else:
                    second_point = cluster2[j - len(cluster1)]
                
            else:
                # the first point
                if i < len(cluster1):
                    first_point = data[cluster1[i]]
                else:
                    first_point = data[cluster2[i - len(cluster1)]]
            
                if j < len(cluster1):
                    second_point = data[cluster1[j]]
                else:
                    second_point = data[cluster2[j - len(cluster1)]]
            
            distance += euclidean_distance_square(first_point, second_point)
    
    distance /= float((len(cluster1) + len(cluster2)) * (len(cluster1) + len(cluster2) - 1.0))
    return distance ** 0.5