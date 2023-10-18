def update(self, iterations=10):
        
        """ Iterates the graph layout and updates node positions.
        """    
        
        # The graph fades in when initially constructed.
        self.alpha += 0.05
        self.alpha = min(self.alpha, 1.0)

        # Iterates over the graph's layout.
        # Each step the graph's bounds are recalculated
        # and a number of iterations are processed,
        # more and more as the layout progresses.
        if self.layout.i == 0:
            self.layout.prepare()
            self.layout.i += 1
        elif self.layout.i == 1:
            self.layout.iterate()
        elif self.layout.i < self.layout.n:
            n = min(iterations, self.layout.i / 10 + 1)
            for i in range(n): 
                self.layout.iterate()
        
        # Calculate the absolute center of the graph.
        min_, max = self.layout.bounds
        self.x = _ctx.WIDTH - max.x*self.d - min_.x*self.d
        self.y = _ctx.HEIGHT - max.y*self.d - min_.y*self.d
        self.x /= 2
        self.y /= 2
            
        return not self.layout.done