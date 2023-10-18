def insert(self, entry):
        """!
        @brief Insert clustering feature to the tree.
        
        @param[in] entry (cfentry): Clustering feature that should be inserted.
        
        """
                
        if (self.__root is None):
            node = leaf_node(entry, None, [ entry ], None);
            
            self.__root = node;
            self.__leafes.append(node);
            
            # Update statistics
            self.__amount_entries += 1;
            self.__amount_nodes += 1;
            self.__height += 1;             # root has successor now
        else:
            child_node_updation = self.__recursive_insert(entry, self.__root);
            if (child_node_updation is True):
                # Splitting has been finished, check for possibility to merge (at least we have already two children).
                if (self.__merge_nearest_successors(self.__root) is True):
                    self.__amount_nodes -= 1;