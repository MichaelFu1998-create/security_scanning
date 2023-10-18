def positions(self):
        '''List of positions for linear degrees of freedom.'''
        return [self.ode_obj.getPosition(i) for i in range(self.LDOF)]