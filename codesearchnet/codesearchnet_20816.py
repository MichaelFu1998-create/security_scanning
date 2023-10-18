def erps(self, erps):
        '''Set the ERP values for this object's degrees of freedom.

        Parameters
        ----------
        erps : float or sequence of float
            An ERP value to set on all degrees of freedom, or a list
            containing one such value for each degree of freedom.
        '''
        _set_params(self.ode_obj, 'ERP', erps, self.ADOF + self.LDOF)