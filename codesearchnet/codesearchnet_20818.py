def stop_cfms(self, stop_cfms):
        '''Set the CFM values for this object's DOF limits.

        Parameters
        ----------
        stop_cfms : float or sequence of float
            A CFM value to set on all degrees of freedom limits, or a list
            containing one such value for each degree of freedom limit.
        '''
        _set_params(self.ode_obj, 'StopCFM', stop_cfms, self.ADOF + self.LDOF)