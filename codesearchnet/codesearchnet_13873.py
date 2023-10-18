def apply(self):
        """ Check the rules for each node in the graph and apply the style.
        """
        sorted = self.order + self.keys()
        unique = []; [unique.append(x) for x in sorted if x not in unique]
        for node in self.graph.nodes:
            for s in unique:
                if self.has_key(s) and self[s](self.graph, node): 
                    node.style = s