def add_edge(self, id1, id2, weight=0.0, length=1.0, label="", properties={}):
        
        """ Add weighted (0.0-1.0) edge between nodes, creating them if necessary.
        The weight represents the importance of the connection (not the cost).
        """
        
        if id1 == id2: return None
        
        if not self.has_key(id1): self.add_node(id1)
        if not self.has_key(id2): self.add_node(id2)
        n1 = self[id1]
        n2 = self[id2]
        
        # If a->b already exists, don't re-create it.
        # However, b->a may still pass.
        if n1 in n2.links:
            if n2.links.edge(n1).node1 == n1:
                return self.edge(id1, id2)

        weight = max(0.0, min(weight, 1.0))

        e = edge(n1, n2, weight, length, label, properties)
        self.edges.append(e)    
        n1.links.append(n2, e)
        n2.links.append(n1, e)

        return e