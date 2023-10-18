def axes(self, axes):
        '''Set the linear axis of displacement for this joint.

        Parameters
        ----------
        axes : list containing one 3-tuple of floats
            A list of the axes for this joint. For a slider joint, which has one
            degree of freedom, this must contain one 3-tuple specifying the X,
            Y, and Z axis for the joint.
        '''
        self.lmotor.axes = [axes[0]]
        self.ode_obj.setAxis(tuple(axes[0]))