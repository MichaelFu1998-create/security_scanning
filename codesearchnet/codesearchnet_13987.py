def alignment(self, d=5):
        
        """ Boids match velocity with other boids.
        """
        
        vx = vy = vz = 0
        for b in self.boids:
           if b != self:
               vx, vy, vz = vx+b.vx, vy+b.vy, vz+b.vz
        
        n = len(self.boids)-1
        vx, vy, vz = vx/n, vy/n, vz/n
        
        return (vx-self.vx)/d, (vy-self.vy)/d, (vz-self.vz)/d