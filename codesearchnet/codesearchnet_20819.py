def stop_erps(self, stop_erps):
        '''Set the ERP values for this object's DOF limits.

        Parameters
        ----------
        stop_erps : float or sequence of float
            An ERP value to set on all degrees of freedom limits, or a list
            containing one such value for each degree of freedom limit.
        '''
        _set_params(self.ode_obj, 'StopERP', stop_erps, self.ADOF + self.LDOF)