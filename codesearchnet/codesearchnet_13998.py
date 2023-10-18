def clear(self):
        
        """ Remove nodes and edges and reset the layout.
        """
        
        dict.clear(self)
        self.nodes = []
        self.edges = []
        self.root  = None
        
        self.layout.i = 0
        self.alpha = 0