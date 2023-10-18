def merge(self, node):
        """!
        @brief Merge leaf node to the current.
        
        @param[in] node (leaf_node): Leaf node that should be merged with current.
        
        """
        
        self.feature += node.feature;
        
        # Move entries from merged node
        for entry in node.entries:
            self.entries.append(entry);