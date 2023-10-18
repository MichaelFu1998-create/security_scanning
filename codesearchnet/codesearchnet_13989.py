def _angle(self):
        
        """ Returns the angle towards which the boid is steering.
        """
        
        from math import atan, pi, degrees
        a = degrees(atan(self.vy/self.vx)) + 360
        if self.vx < 0: a += 180

        return a