def draw(self, dx=0, dy=0, weighted=False, directed=False, highlight=[], traffic=None):
        
        """ Layout the graph incrementally.
        
        The graph is drawn at the center of the canvas.
        The weighted and directed parameters visualize edge weight and direction.
        The highlight specifies list of connected nodes. 
        The path will be colored according to the "highlight" style.
        Clicking and dragging events are monitored.
        
        """
        
        self.update()

        # Draw the graph background.
        s = self.styles.default
        s.graph_background(s)

        # Center the graph on the canvas.
        _ctx.push()
        _ctx.translate(self.x+dx, self.y+dy)
 
        # Indicate betweenness centrality.
        if traffic:
            if isinstance(traffic, bool): 
                traffic = 5
            for n in self.nodes_by_betweenness()[:traffic]:
                try: s = self.styles[n.style]
                except: s = self.styles.default
                if s.graph_traffic:
                    s.graph_traffic(s, n, self.alpha)        

        # Draw the edges and their labels.
        s = self.styles.default
        if s.edges:
            s.edges(s, self.edges, self.alpha, weighted, directed)
        
        # Draw each node in the graph.
        # Apply individual style to each node (or default).        
        for n in self.nodes:
            try:  s = self.styles[n.style]
            except: s = self.styles.default
            if s.node:
                s.node(s, n, self.alpha)
        
        # Highlight the given shortest path.
        try: s = self.styles.highlight
        except: s = self.styles.default
        if s.path:
            s.path(s, self, highlight)

        # Draw node id's as labels on each node.
        for n in self.nodes:
            try:  s = self.styles[n.style]
            except: s = self.styles.default
            if s.node_label:
                s.node_label(s, n, self.alpha)
        
        # Events for clicked and dragged nodes.
        # Nodes will resist being dragged by attraction and repulsion,
        # put the event listener on top to get more direct feedback.
        #self.events.update()
        
        _ctx.pop()