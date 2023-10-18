def separation(self, r=10):
        
        """ Boids keep a small distance from other boids.
        
        Ensures that boids don't collide into each other,
        in a smoothly accelerated motion.
        
        """
        
        vx = vy = vz = 0
        for b in self.boids:
            if b != self:
                if abs(self.x-b.x) < r: vx += (self.x-b.x)
                if abs(self.y-b.y) < r: vy += (self.y-b.y)
                if abs(self.z-b.z) < r: vz += (self.z-b.z)
                
        return vx, vy, vz