def __merge_clusters(self, cluster1, cluster2):
        """!
        @brief Merges two clusters and returns new merged cluster. Representation points and mean points are calculated for the new cluster.
        
        @param[in] cluster1 (cure_cluster): Cluster that should be merged.
        @param[in] cluster2 (cure_cluster): Cluster that should be merged.
        
        @return (cure_cluster) New merged CURE cluster.
        
        """
        
        merged_cluster = cure_cluster(None, None)
        
        merged_cluster.points = cluster1.points + cluster2.points
        merged_cluster.indexes = cluster1.indexes + cluster2.indexes
        
        # merged_cluster.mean = ( len(cluster1.points) * cluster1.mean + len(cluster2.points) * cluster2.mean ) / ( len(cluster1.points) + len(cluster2.points) );
        dimension = len(cluster1.mean)
        merged_cluster.mean = [0] * dimension
        if merged_cluster.points[1:] == merged_cluster.points[:-1]:
            merged_cluster.mean = merged_cluster.points[0]
        else:
            for index in range(dimension):
                merged_cluster.mean[index] = ( len(cluster1.points) * cluster1.mean[index] + len(cluster2.points) * cluster2.mean[index] ) / ( len(cluster1.points) + len(cluster2.points) );
        
        temporary = list()
        
        for index in range(self.__number_represent_points):
            maximal_distance = 0
            maximal_point = None
            
            for point in merged_cluster.points:
                minimal_distance = 0
                if index == 0:
                    minimal_distance = euclidean_distance_square(point, merged_cluster.mean)
                    #minimal_distance = euclidean_distance_sqrt(point, merged_cluster.mean);
                else:
                    minimal_distance = min([euclidean_distance_square(point, p) for p in temporary])
                    #minimal_distance = cluster_distance(cure_cluster(point), cure_cluster(temporary[0]));
                    
                if minimal_distance >= maximal_distance:
                    maximal_distance = minimal_distance
                    maximal_point = point
        
            if maximal_point not in temporary:
                temporary.append(maximal_point)
                
        for point in temporary:
            representative_point = [0] * dimension
            for index in range(dimension):
                representative_point[index] = point[index] + self.__compression * (merged_cluster.mean[index] - point[index])
                
            merged_cluster.rep.append(representative_point)
        
        return merged_cluster