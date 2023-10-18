def update(self):
        
        """ Rotates the queued texts and determines display time.
        """
        
        if self.delay > 0:
            # It takes a while for the popup to appear.
            self.delay -= 1; return
            
        if self.fi == 0:
            # Only one text in queue, displayed infinitely.
            if len(self.q) == 1: 
                self.fn = float("inf")
            # Else, display time depends on text length.
            else:
                self.fn = len(self.q[self.i]) / self.speed
                self.fn = max(self.fn, self.mf)            
            
        self.fi += 1
        if self.fi > self.fn:
            # Rotate to the next text in queue.
            self.fi = 0
            self.i = (self.i+1) % len(self.q)