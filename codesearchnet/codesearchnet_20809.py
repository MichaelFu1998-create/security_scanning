def angle_rates(self):
        '''List of angle rates for rotational degrees of freedom.'''
        return [self.ode_obj.getAngleRate(i) for i in range(self.ADOF)]