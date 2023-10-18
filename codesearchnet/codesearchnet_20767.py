def find(self, *args):
        """
        Find a node in the tree. If the node is not found it is added first and then returned.

        :param args: a tuple
        :return: returns the node
        """
        curr_node = self.__root
        return self.__traverse(curr_node, 0,  *args)