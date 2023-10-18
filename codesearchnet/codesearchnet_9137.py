def find(self, y):
        """Returns starting position of the substring y in the string used for
        building the Suffix tree.

        :param y: String
        :return: Index of the starting position of string y in the string used for building the Suffix tree
                 -1 if y is not a substring.
        """
        node = self.root
        while True:
            edge = self._edgeLabel(node, node.parent)
            if edge.startswith(y):
                return node.idx
            
            i = 0
            while(i < len(edge) and edge[i] == y[0]):
                y = y[1:]
                i += 1
            
            if i != 0:
                if i == len(edge) and y != '':
                    pass
                else:
                    return -1
            
            node = node._get_transition_link(y[0])
            if not node:
                return -1