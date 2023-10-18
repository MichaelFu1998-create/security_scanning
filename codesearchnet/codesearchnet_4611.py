def __optimize_configuration(self):
        """!
        @brief Finds quasi-optimal medoids and updates in line with them clusters in line with algorithm's rules. 
        
        """
        index_neighbor = 0
        while (index_neighbor < self.__maxneighbor):
            # get random current medoid that is to be replaced
            current_medoid_index = self.__current[random.randint(0, self.__number_clusters - 1)]
            current_medoid_cluster_index = self.__belong[current_medoid_index]
            
            # get new candidate to be medoid
            candidate_medoid_index = random.randint(0, len(self.__pointer_data) - 1)
            
            while candidate_medoid_index in self.__current:
                candidate_medoid_index = random.randint(0, len(self.__pointer_data) - 1)
            
            candidate_cost = 0.0
            for point_index in range(0, len(self.__pointer_data)):
                if point_index not in self.__current:
                    # get non-medoid point and its medoid
                    point_cluster_index = self.__belong[point_index]
                    point_medoid_index = self.__current[point_cluster_index]
                    
                    # get other medoid that is nearest to the point (except current and candidate)
                    other_medoid_index = self.__find_another_nearest_medoid(point_index, current_medoid_index)
                    other_medoid_cluster_index = self.__belong[other_medoid_index]
                    
                    # for optimization calculate all required distances
                    # from the point to current medoid
                    distance_current = euclidean_distance_square(self.__pointer_data[point_index], self.__pointer_data[current_medoid_index])
                    
                    # from the point to candidate median
                    distance_candidate = euclidean_distance_square(self.__pointer_data[point_index], self.__pointer_data[candidate_medoid_index])
                    
                    # from the point to nearest (own) medoid
                    distance_nearest = float('inf')
                    if ( (point_medoid_index != candidate_medoid_index) and (point_medoid_index != current_medoid_cluster_index) ):
                        distance_nearest = euclidean_distance_square(self.__pointer_data[point_index], self.__pointer_data[point_medoid_index])
                    
                    # apply rules for cost calculation
                    if (point_cluster_index == current_medoid_cluster_index):
                        # case 1:
                        if (distance_candidate >= distance_nearest):
                            candidate_cost += distance_nearest - distance_current
                        
                        # case 2:
                        else:
                            candidate_cost += distance_candidate - distance_current
                    
                    elif (point_cluster_index == other_medoid_cluster_index):
                        # case 3 ('nearest medoid' is the representative object of that cluster and object is more similar to 'nearest' than to 'candidate'):
                        if (distance_candidate > distance_nearest):
                            pass;
                        
                        # case 4:
                        else:
                            candidate_cost += distance_candidate - distance_nearest
            
            if (candidate_cost < 0):
                # set candidate that has won
                self.__current[current_medoid_cluster_index] = candidate_medoid_index
                
                # recalculate clusters
                self.__update_clusters(self.__current)
                
                # reset iterations and starts investigation from the begining
                index_neighbor = 0
                
            else:
                index_neighbor += 1