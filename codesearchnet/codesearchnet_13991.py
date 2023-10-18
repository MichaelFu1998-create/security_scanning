def constrain(self):
        
        """ Cages the flock inside the x, y, w, h area.
        
        The actual cage is a bit larger,
        so boids don't seem to bounce of invisible walls
        (they are rather "encouraged" to stay in the area).
        
        If a boid touches the ground level,
        it may decide to perch there for a while.
        
        """
        
        dx = self.w * 0.1
        dy = self.h * 0.1 
        
        for b in self:
            
            if b.x < self.x-dx: b.vx += _ctx.random(dx)
            if b.y < self.y-dy: b.vy += _ctx.random(dy)
            if b.x > self.x+self.w+dx: b.vx -= _ctx.random(dx)
            if b.y > self.y+self.h+dy: b.vy -= _ctx.random(dy)
            if b.z < 0: b.vz += 10
            if b.z > 100: b.vz -= 10
            
            if b.y > self._perch_y and _ctx.random() < self._perch:
                b.y = self._perch_y
                b.vy = -abs(b.vy) * 0.2
                b.is_perching = True
                try:
                    b._perch_t = self._perch_t()
                except:
                    b._perch_t = self._perch_t