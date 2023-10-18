def load(self, id):
        
        """ Rebuilds the graph around the given node id.
        """
        
        self.clear()
    
        # Root node.
        self.add_node(id, root=True)
    
        # Directly connected nodes have priority.
        for w, id2 in self.get_links(id):
            self.add_edge(id, id2, weight=w)
            if len(self) > self.max: 
                break

        # Now get all the other nodes in the cluster.
        for w, id2, links in self.get_cluster(id):
            for id3 in links:
                self.add_edge(id3, id2, weight=w)
                self.add_edge(id, id3, weight=w)
            #if len(links) == 0:
            #    self.add_edge(id, id2)
            if len(self) > self.max: 
                break    

        # Provide a backlink to the previous root.
        if self.event.clicked: 
            g.add_node(self.event.clicked)