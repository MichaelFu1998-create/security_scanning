def update(self, 
               shuffled=True, 
               cohesion=100, 
               separation=10, 
               alignment=5, 
               goal=20,
               limit=30):
        
        """ Calculates the next motion frame for the flock.
        """
        
        # Shuffling the list of boids ensures fluid movement.
        # If you need the boids to retain their position in the list
        # each update, set the shuffled parameter to False.
        from random import shuffle
        if shuffled: shuffle(self)
        
        m1 = 1.0 # cohesion
        m2 = 1.0 # separation
        m3 = 1.0 # alignment
        m4 = 1.0 # goal
        
        # The flock scatters randomly with a Boids.scatter chance.
        # This means their cohesion (m1) is reversed,
        # and their joint alignment (m3) is dimished,
        # causing boids to oscillate in confusion.
        # Setting Boids.scatter(chance=0) ensures they never scatter.
        if not self.scattered and _ctx.random() < self._scatter:
            self.scattered = True
        if self.scattered:
            m1 = -m1
            m3 *= 0.25
            self._scatter_i += 1
        if self._scatter_i >= self._scatter_t:
            self.scattered = False
            self._scatter_i = 0

        # A flock can have a goal defined with Boids.goal(x,y,z),
        # a place of interest to flock around.
        if not self.has_goal:
            m4 = 0
        if self.flee:
            m4 = -m4
        
        for b in self:
            
            # A boid that is perching will continue to do so
            # until Boid._perch_t reaches zero.
            if b.is_perching:
                if b._perch_t > 0:
                    b._perch_t -= 1
                    continue
                else:
                    b.is_perching = False
            
            vx1, vy1, vz1 = b.cohesion(cohesion)
            vx2, vy2, vz2 = b.separation(separation)
            vx3, vy3, vz3 = b.alignment(alignment)
            vx4, vy4, vz4 = b.goal(self._gx, self._gy, self._gz, goal)
            
            b.vx += m1*vx1 + m2*vx2 + m3*vx3 + m4*vx4
            b.vy += m1*vy1 + m2*vy2 + m3*vy3 + m4*vy4
            b.vz += m1*vz1 + m2*vz2 + m3*vz3 + m4*vz4
            
            b.limit(limit)
        
            b.x += b.vx
            b.y += b.vy
            b.z += b.vz
        
        self.constrain()