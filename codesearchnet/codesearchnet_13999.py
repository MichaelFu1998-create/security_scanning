def add_node(self, id, radius=8, style=style.DEFAULT, category="", label=None, root=False,
                 properties={}):
        
        """ Add node from id and return the node object.
        """
        
        if self.has_key(id): 
            return self[id]
            
        if not isinstance(style, str) and style.__dict__.has_key["name"]:
            style = style.name
        
        n = node(self, id, radius, style, category, label, properties)
        self[n.id] = n
        self.nodes.append(n)
        if root: self.root = n
            
        return n