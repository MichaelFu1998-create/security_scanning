def __split_procedure(self, split_node):
        """!
        @brief Starts node splitting procedure in the CF-tree from the specify node.
        
        @param[in] split_node (cfnode): CF-tree node that should be splitted.
        
        """
        if (split_node is self.__root):
            self.__root = non_leaf_node(split_node.feature, None, [ split_node ], None);
            split_node.parent = self.__root;
            
            # Update statistics
            self.__amount_nodes += 1;
            self.__height += 1;
        
        [new_node1, new_node2] = self.__split_leaf_node(split_node);
        
        self.__leafes.remove(split_node);
        self.__leafes.append(new_node1);
        self.__leafes.append(new_node2);
        
        # Update parent list of successors
        parent = split_node.parent;
        parent.successors.remove(split_node);
        parent.successors.append(new_node1);
        parent.successors.append(new_node2);
        
        # Update statistics
        self.__amount_nodes += 1;