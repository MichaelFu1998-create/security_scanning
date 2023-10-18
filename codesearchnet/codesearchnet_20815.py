def max_forces(self, max_forces):
        '''Set the maximum forces for this object's degrees of freedom.

        Parameters
        ----------
        max_forces : float or sequence of float
            A maximum force value to set on all degrees of freedom, or a list
            containing one such value for each degree of freedom.
        '''
        _set_params(self.ode_obj, 'FMax', max_forces, self.ADOF + self.LDOF)