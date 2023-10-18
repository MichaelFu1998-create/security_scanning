def limit(self, max=30):
        
        """ The speed limit for a boid.
        
        Boids can momentarily go very fast,
        something that is impossible for real animals.
        
        """
        
        if abs(self.vx) > max: 
            self.vx = self.vx/abs(self.vx)*max
        if abs(self.vy) > max: 
            self.vy = self.vy/abs(self.vy)*max
        if abs(self.vz) > max: 
            self.vz = self.vz/abs(self.vz)*max