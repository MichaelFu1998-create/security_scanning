def velocities(self, velocities):
        '''Set the target velocities for this object's degrees of freedom.

        Parameters
        ----------
        velocities : float or sequence of float
            A target velocity value to set on all degrees of freedom, or a list
            containing one such value for each degree of freedom. For rotational
            degrees of freedom, these values must be in radians / second.
        '''
        _set_params(self.ode_obj, 'Vel', velocities, self.ADOF + self.LDOF)