def angles(self):
        '''List of angles for rotational degrees of freedom.'''
        return [self.ode_obj.getAngle(i) for i in range(self.ADOF)]