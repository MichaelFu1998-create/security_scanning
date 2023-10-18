def remove(self, point, **kwargs):
        """!
        @brief Remove specified point from kd-tree.
        @details It removes the first found node that satisfy to the input parameters. Make sure that
                  pair (point, payload) is unique for each node, othewise the first found is removed.
        
        @param[in] point (list): Coordinates of the point of removed node.
        @param[in] **kwargs: Arbitrary keyword arguments (available arguments: 'payload').
        
        <b>Keyword Args:</b><br>
            - payload (any): Payload of the node that should be removed.
        
        @return (node) Root if node has been successfully removed, otherwise None.
        
        """
        
        # Get required node
        node_for_remove = None
        if 'payload' in kwargs:
            node_for_remove = self.find_node_with_payload(point, kwargs['payload'], None)
        else:
            node_for_remove = self.find_node(point, None)
        
        if node_for_remove is None:
            return None
        
        parent = node_for_remove.parent
        minimal_node = self.__recursive_remove(node_for_remove)
        if parent is None:
            self.__root = minimal_node
            
            # If all k-d tree was destroyed
            if minimal_node is not None:
                minimal_node.parent = None
        else:
            if parent.left is node_for_remove:
                parent.left = minimal_node
            elif parent.right is node_for_remove:
                parent.right = minimal_node
        
        return self.__root