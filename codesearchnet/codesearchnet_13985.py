def cohesion(self, d=100):
        
        """ Boids move towards the flock's centre of mass.
        
        The centre of mass is the average position of all boids,
        not including itself (the "perceived centre").
        
        """
        
        vx = vy = vz = 0
        for b in self.boids:
            if b != self:
                vx, vy, vz = vx+b.x, vy+b.y, vz+b.z
                
        n = len(self.boids)-1
        vx, vy, vz = vx/n, vy/n, vz/n
        
        return (vx-self.x)/d, (vy-self.y)/d, (vz-self.z)/d