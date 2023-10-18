def __expand_cluster_order(self, optics_object):
        """!
        @brief Expand cluster order from not processed optic-object that corresponds to object from input data.
               Traverse procedure is performed until objects are reachable from core-objects in line with connectivity radius.
               Order database is updated during expanding.
               
        @param[in] optics_object (optics_descriptor): Object that hasn't been processed.
        
        """
        
        optics_object.processed = True
        
        neighbors_descriptor = self.__neighbor_searcher(optics_object)
        optics_object.reachability_distance = None
        
        self.__ordered_database.append(optics_object)
        
        # Check core distance
        if len(neighbors_descriptor) >= self.__minpts:
            neighbors_descriptor.sort(key = lambda obj: obj[1])
            optics_object.core_distance = neighbors_descriptor[self.__minpts - 1][1]
            
            # Continue processing
            order_seed = list()
            self.__update_order_seed(optics_object, neighbors_descriptor, order_seed)
            
            while len(order_seed) > 0:
                optic_descriptor = order_seed[0]
                order_seed.remove(optic_descriptor)
                
                neighbors_descriptor = self.__neighbor_searcher(optic_descriptor)
                optic_descriptor.processed = True
                
                self.__ordered_database.append(optic_descriptor)
                
                if len(neighbors_descriptor) >= self.__minpts:
                    neighbors_descriptor.sort(key = lambda obj: obj[1])
                    optic_descriptor.core_distance = neighbors_descriptor[self.__minpts - 1][1]
                    
                    self.__update_order_seed(optic_descriptor, neighbors_descriptor, order_seed)
                else:
                    optic_descriptor.core_distance = None
                    
        else:
            optics_object.core_distance = None