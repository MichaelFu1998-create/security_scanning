def __split_leaf_node(self, node):
        """!
        @brief Performs splitting of the specified leaf node.
        
        @param[in] node (leaf_node): Leaf node that should be splitted.
        
        @return (list) New pair of leaf nodes [leaf_node1, leaf_node2].
        
        @warning Splitted node is transformed to non_leaf.
        
        """
        
        # search farthest pair of entries
        [farthest_entity1, farthest_entity2] = node.get_farthest_entries(self.__type_measurement);
                    
        # create new nodes
        new_node1 = leaf_node(farthest_entity1, node.parent, [ farthest_entity1 ], None);
        new_node2 = leaf_node(farthest_entity2, node.parent, [ farthest_entity2 ], None);
        
        # re-insert other entries
        for entity in node.entries:
            if ( (entity is not farthest_entity1) and (entity is not farthest_entity2) ):
                distance1 = new_node1.feature.get_distance(entity, self.__type_measurement);
                distance2 = new_node2.feature.get_distance(entity, self.__type_measurement);
                
                if (distance1 < distance2):
                    new_node1.insert_entry(entity);
                else:
                    new_node2.insert_entry(entity);
        
        return [new_node1, new_node2];