def axes(self):
        '''List of axes for this object's degrees of freedom.'''
        return [np.array(self.ode_obj.getAxis(i))
                for i in range(self.ADOF or self.LDOF)]