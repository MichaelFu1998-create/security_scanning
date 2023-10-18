def children(self, node_parent):
        """!
        @brief Returns list of children of node.
        
        @param[in] node_parent (node): Node whose children are required. 
        
        @return (list) Children of node. If node haven't got any child then None is returned.
        
        """
        
        if node_parent.left is not None:
            yield node_parent.left
        if node_parent.right is not None:
            yield node_parent.right