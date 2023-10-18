def __update_order_seed(self, optic_descriptor, neighbors_descriptors, order_seed):
        """!
        @brief Update sorted list of reachable objects (from core-object) that should be processed using neighbors of core-object.
        
        @param[in] optic_descriptor (optics_descriptor): Core-object whose neighbors should be analysed.
        @param[in] neighbors_descriptors (list): List of neighbors of core-object.
        @param[in|out] order_seed (list): List of sorted object in line with reachable distance.
        
        """
        
        for neighbor_descriptor in neighbors_descriptors:
            index_neighbor = neighbor_descriptor[0]
            current_reachable_distance = neighbor_descriptor[1]
            
            if self.__optics_objects[index_neighbor].processed is not True:
                reachable_distance = max(current_reachable_distance, optic_descriptor.core_distance)
                if self.__optics_objects[index_neighbor].reachability_distance is None:
                    self.__optics_objects[index_neighbor].reachability_distance = reachable_distance
                    
                    # insert element in queue O(n) - worst case.
                    index_insertion = len(order_seed)
                    for index_seed in range(0, len(order_seed)):
                        if reachable_distance < order_seed[index_seed].reachability_distance:
                            index_insertion = index_seed
                            break
                    
                    order_seed.insert(index_insertion, self.__optics_objects[index_neighbor])

                else:
                    if reachable_distance < self.__optics_objects[index_neighbor].reachability_distance:
                        self.__optics_objects[index_neighbor].reachability_distance = reachable_distance
                        order_seed.sort(key = lambda obj: obj.reachability_distance)