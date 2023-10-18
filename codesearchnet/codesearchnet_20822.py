def axes(self, axes):
        '''Set the angular axis of rotation for this joint.

        Parameters
        ----------
        axes : list containing one 3-tuple of floats
            A list of the axes for this joint. For a hinge joint, which has one
            degree of freedom, this must contain one 3-tuple specifying the X,
            Y, and Z axis for the joint.
        '''
        self.amotor.axes = [axes[0]]
        self.ode_obj.setAxis(tuple(axes[0]))