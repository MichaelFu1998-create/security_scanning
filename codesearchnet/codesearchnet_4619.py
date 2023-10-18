def insert(self, point, payload):
        """!
        @brief Insert new point with payload to kd-tree.
        
        @param[in] point (list): Coordinates of the point of inserted node.
        @param[in] payload (any-type): Payload of inserted node. It can be identificator of the node or
                    some useful payload that belongs to the point.
        
        @return (node) Inserted node to the kd-tree.
        
        """
        
        if self.__root is None:
            self.__dimension = len(point)
            self.__root = node(point, payload, None, None, 0)
            self.__point_comparator = self.__create_point_comparator(type(point))
            return self.__root
        
        cur_node = self.__root
        
        while True:
            if cur_node.data[cur_node.disc] <= point[cur_node.disc]:
                # If new node is greater or equal than current node then check right leaf
                if cur_node.right is None:
                    discriminator = cur_node.disc + 1
                    if discriminator >= self.__dimension:
                        discriminator = 0
                        
                    cur_node.right = node(point, payload, None, None, discriminator, cur_node)
                    return cur_node.right
                else: 
                    cur_node = cur_node.right
            
            else:
                # If new node is less than current then check left leaf
                if cur_node.left is None:
                    discriminator = cur_node.disc + 1
                    if discriminator >= self.__dimension:
                        discriminator = 0
                        
                    cur_node.left = node(point, payload, None, None, discriminator, cur_node)
                    return cur_node.left
                else:
                    cur_node = cur_node.left