def __insert_for_noneleaf_node(self, entry, search_node):
        """!
        @brief Recursive insert entry from none-leaf node to the tree.
        
        @param[in] entry (cfentry): Clustering feature.
        @param[in] search_node (cfnode): None-leaf node from that insertion should be started.
        
        @return (bool) True if number of nodes at the below level is changed, otherwise False.
        
        """
        
        node_amount_updation = False;
        
        min_key = lambda child_node: child_node.get_distance(search_node, self.__type_measurement);
        nearest_child_node = min(search_node.successors, key = min_key);
        
        child_node_updation = self.__recursive_insert(entry, nearest_child_node);
        
        # Update clustering feature of none-leaf node.
        search_node.feature += entry;
            
        # Check branch factor, probably some leaf has been splitted and threshold has been exceeded.
        if (len(search_node.successors) > self.__branch_factor):
            
            # Check if it's aleady root then new root should be created (height is increased in this case).
            if (search_node is self.__root):
                self.__root = non_leaf_node(search_node.feature, None, [ search_node ], None);
                search_node.parent = self.__root;
                
                # Update statistics
                self.__amount_nodes += 1;
                self.__height += 1;
                
            [new_node1, new_node2] = self.__split_nonleaf_node(search_node);
            
            # Update parent list of successors
            parent = search_node.parent;
            parent.successors.remove(search_node);
            parent.successors.append(new_node1);
            parent.successors.append(new_node2);
            
            # Update statistics
            self.__amount_nodes += 1;
            node_amount_updation = True;
            
        elif (child_node_updation is True):
            # Splitting has been finished, check for possibility to merge (at least we have already two children).
            if (self.__merge_nearest_successors(search_node) is True):
                self.__amount_nodes -= 1;
        
        return node_amount_updation;