def __rebuild_tree(self, index_point):
        """!
        @brief Rebuilt tree in case of maxumum number of entries is exceeded.
        
        @param[in] index_point (uint): Index of point that is used as end point of re-building.
        
        @return (cftree) Rebuilt tree with encoded points till specified point from input data space.
        
        """
        
        rebuild_result = False;
        increased_diameter = self.__tree.threshold * self.__diameter_multiplier;
        
        tree = None;
        
        while(rebuild_result is False):
            # increase diameter and rebuild tree
            if (increased_diameter == 0.0):
                increased_diameter = 1.0;
            
            # build tree with update parameters
            tree = cftree(self.__tree.branch_factor, self.__tree.max_entries, increased_diameter, self.__tree.type_measurement);
            
            for index_point in range(0, index_point + 1):
                point = self.__pointer_data[index_point];
                tree.insert_cluster([point]);
            
                if (tree.amount_entries > self.__entry_size_limit):
                    increased_diameter *= self.__diameter_multiplier;
                    continue;
            
            # Re-build is successful.
            rebuild_result = True;
        
        return tree;