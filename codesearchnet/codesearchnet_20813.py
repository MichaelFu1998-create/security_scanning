def hi_stops(self, hi_stops):
        '''Set the hi stop values for this object's degrees of freedom.

        Parameters
        ----------
        hi_stops : float or sequence of float
            A hi stop value to set on all degrees of freedom, or a list
            containing one such value for each degree of freedom. For rotational
            degrees of freedom, these values must be in radians.
        '''
        _set_params(self.ode_obj, 'HiStop', hi_stops, self.ADOF + self.LDOF)