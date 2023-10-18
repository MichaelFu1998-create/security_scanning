def cfms(self, cfms):
        '''Set the CFM values for this object's degrees of freedom.

        Parameters
        ----------
        cfms : float or sequence of float
            A CFM value to set on all degrees of freedom, or a list
            containing one such value for each degree of freedom.
        '''
        _set_params(self.ode_obj, 'CFM', cfms, self.ADOF + self.LDOF)