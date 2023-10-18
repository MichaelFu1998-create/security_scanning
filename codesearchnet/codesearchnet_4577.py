def variance_increase_distance(cluster1, cluster2, data = None):
    """!
    @brief Calculates variance increase distance between two clusters.
    @details Clusters can be represented by list of coordinates (in this case data shouldn't be specified),
             or by list of indexes of points from the data (represented by list of points), in this case 
             data should be specified.
    
    @param[in] cluster1 (list): The first cluster.
    @param[in] cluster2 (list): The second cluster.
    @param[in] data (list): If specified than elements of clusters will be used as indexes,
               otherwise elements of cluster will be considered as points.
    
    @return (double) Average variance increase distance between two clusters.
    
    """
    
    # calculate local sum
    if data is None:
        member_cluster1 = [0.0] * len(cluster1[0])
        member_cluster2 = [0.0] * len(cluster2[0])
        
    else:
        member_cluster1 = [0.0] * len(data[0])
        member_cluster2 = [0.0] * len(data[0])
    
    for i in range(len(cluster1)):
        if data is None:
            member_cluster1 = list_math_addition(member_cluster1, cluster1[i])
        else:
            member_cluster1 = list_math_addition(member_cluster1, data[ cluster1[i] ])

    for j in range(len(cluster2)):
        if data is None:
            member_cluster2 = list_math_addition(member_cluster2, cluster2[j])
        else:
            member_cluster2 = list_math_addition(member_cluster2, data[ cluster2[j] ])
    
    member_cluster_general = list_math_addition(member_cluster1, member_cluster2)
    member_cluster_general = list_math_division_number(member_cluster_general, len(cluster1) + len(cluster2))
    
    member_cluster1 = list_math_division_number(member_cluster1, len(cluster1))
    member_cluster2 = list_math_division_number(member_cluster2, len(cluster2))
    
    # calculate global sum
    distance_general = 0.0
    distance_cluster1 = 0.0
    distance_cluster2 = 0.0
    
    for i in range(len(cluster1)):
        if data is None:
            distance_cluster1 += euclidean_distance_square(cluster1[i], member_cluster1)
            distance_general += euclidean_distance_square(cluster1[i], member_cluster_general)
            
        else:
            distance_cluster1 += euclidean_distance_square(data[ cluster1[i]], member_cluster1)
            distance_general += euclidean_distance_square(data[ cluster1[i]], member_cluster_general)
    
    for j in range(len(cluster2)):
        if data is None:
            distance_cluster2 += euclidean_distance_square(cluster2[j], member_cluster2)
            distance_general += euclidean_distance_square(cluster2[j], member_cluster_general)
            
        else:
            distance_cluster2 += euclidean_distance_square(data[ cluster2[j]], member_cluster2)
            distance_general += euclidean_distance_square(data[ cluster2[j]], member_cluster_general)
    
    return distance_general - distance_cluster1 - distance_cluster2