def __closest_cluster(self, cluster, distance):
        """!
        @brief Find closest cluster to the specified cluster in line with distance.
        
        @param[in] cluster (cure_cluster): Cluster for which nearest cluster should be found.
        @param[in] distance (double): Closest distance to the previous cluster.
        
        @return (tuple) Pair (nearest CURE cluster, nearest distance) if the nearest cluster has been found, otherwise None is returned.
        
        """
        
        nearest_cluster = None
        nearest_distance = float('inf')

        real_euclidean_distance = distance ** 0.5

        for point in cluster.rep:
            # Nearest nodes should be returned (at least it will return itself).
            nearest_nodes = self.__tree.find_nearest_dist_nodes(point, real_euclidean_distance)
            for (candidate_distance, kdtree_node) in nearest_nodes:
                if (candidate_distance < nearest_distance) and (kdtree_node is not None) and (kdtree_node.payload is not cluster):
                    nearest_distance = candidate_distance
                    nearest_cluster = kdtree_node.payload
                    
        return (nearest_cluster, nearest_distance)