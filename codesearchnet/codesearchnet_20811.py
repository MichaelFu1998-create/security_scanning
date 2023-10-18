def axes(self, axes):
        '''Set the axes for this object's degrees of freedom.

        Parameters
        ----------
        axes : list of axes specifications
            A list of axis values to set. This list must have the same number of
            elements as the degrees of freedom of the underlying ODE object.
            Each element can be

            (a) None, which has no effect on the corresponding axis, or
            (b) three floats specifying the axis to set.
        '''
        assert self.ADOF == len(axes) or self.LDOF == len(axes)
        for i, axis in enumerate(axes):
            if axis is not None:
                self.ode_obj.setAxis(i, 0, axis)