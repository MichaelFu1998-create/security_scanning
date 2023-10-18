def remove_edge(self, id1, id2):
        
        """ Remove edges between nodes with given id's.
        """
        
        for e in list(self.edges):
            if id1 in (e.node1.id, e.node2.id) and \
               id2 in (e.node1.id, e.node2.id):
                e.node1.links.remove(e.node2)
                e.node2.links.remove(e.node1)
                self.edges.remove(e)