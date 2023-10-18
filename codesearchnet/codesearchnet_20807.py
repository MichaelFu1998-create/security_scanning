def position_rates(self):
        '''List of position rates for linear degrees of freedom.'''
        return [self.ode_obj.getPositionRate(i) for i in range(self.LDOF)]