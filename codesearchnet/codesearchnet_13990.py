def goal(self, x, y, z, d=50.0):
        
        """ Tendency towards a particular place.
        """
        
        return (x-self.x)/d, (y-self.y)/d, (z-self.z)/d