def lo_stops(self, lo_stops):
        '''Set the lo stop values for this object's degrees of freedom.

        Parameters
        ----------
        lo_stops : float or sequence of float
            A lo stop value to set on all degrees of freedom, or a list
            containing one such value for each degree of freedom. For rotational
            degrees of freedom, these values must be in radians.
        '''
        _set_params(self.ode_obj, 'LoStop', lo_stops, self.ADOF + self.LDOF)