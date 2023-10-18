def __insert_for_leaf_node(self, entry, search_node):
        """!
        @brief Recursive insert entry from leaf node to the tree.
        
        @param[in] entry (cfentry): Clustering feature.
        @param[in] search_node (cfnode): None-leaf node from that insertion should be started.
        
        @return (bool) True if number of nodes at the below level is changed, otherwise False.
        
        """
        
        node_amount_updation = False;
        
        # Try to absorb by the entity
        index_nearest_entry = search_node.get_nearest_index_entry(entry, self.__type_measurement);
        merged_entry = search_node.entries[index_nearest_entry] + entry;
        
        # Otherwise try to add new entry
        if (merged_entry.get_diameter() > self.__threshold):
            # If it's not exceeded append entity and update feature of the leaf node.
            search_node.insert_entry(entry);
            
            # Otherwise current node should be splitted
            if (len(search_node.entries) > self.__max_entries):
                self.__split_procedure(search_node);
                node_amount_updation = True;
            
            # Update statistics
            self.__amount_entries += 1;
            
        else:
            search_node.entries[index_nearest_entry] = merged_entry;
            search_node.feature += entry;
        
        return node_amount_updation;