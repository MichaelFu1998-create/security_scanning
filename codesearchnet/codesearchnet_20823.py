def axes(self):
        '''A list of axes of rotation for this joint.'''
        return [np.array(self.ode_obj.getAxis1()),
                np.array(self.ode_obj.getAxis2())]