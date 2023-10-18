def axes(self, axes):
        '''Set the axes for this object's degrees of freedom.

        Parameters
        ----------
        axes : list of axis parameters
            A list of axis values to set. This list must have the same number of
            elements as the degrees of freedom of the underlying ODE object.
            Each element can be

            (a) None, which has no effect on the corresponding axis, or
            (b) three floats specifying the axis to set, or
            (c) a dictionary with an "axis" key specifying the axis to set and
                an optional "rel" key (defaults to 0) specifying the relative
                body to set the axis on.
        '''
        assert len(axes) == self.ADOF
        for i, ax in enumerate(axes):
            if ax is None:
                continue
            if not isinstance(ax, dict):
                ax = dict(axis=ax)
            self.ode_obj.setAxis(i, ax.get('rel', 0), ax['axis'])