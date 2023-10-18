def edge(self, id1, id2):
        """ Returns the edge between the nodes with given id1 and id2.
        """
        if id1 in self and \
           id2 in self and \
           self[id2] in self[id1].links:
            return self[id1].links.edge(id2)
        return None