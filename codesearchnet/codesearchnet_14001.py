def remove_node(self, id):
        
        """ Remove node with given id.
        """
 
        if self.has_key(id):
            n = self[id]
            self.nodes.remove(n)
            del self[id]
            
            # Remove all edges involving id and all links to it.
            for e in list(self.edges):
                if n in (e.node1, e.node2):
                    if n in e.node1.links: 
                        e.node1.links.remove(n)
                    if n in e.node2.links: 
                        e.node2.links.remove(n)
                    self.edges.remove(e)