def get_termination_stats(self, get_cos=True):
        """
        Returns a dict of termination statistics

        Parameters
        ----------
            get_cos : Bool, optional
                Whether or not to calcualte the cosine of the residuals
                with the tangent plane of the model using the current J.
                The calculation may take some time. Default is True

        Returns
        -------
            dict
                Has keys
                    delta_vals  : The last change in parameter values.
                    delta_err   : The last change in the error.
                    exp_err     : The expected (last) change in the error.
                    frac_err    : The fractional change in the error.
                    num_iter    : The number of iterations completed.
                    error       : The current error.
        """
        delta_vals = self._last_vals - self.param_vals
        delta_err = self._last_error - self.error
        frac_err = delta_err / self.error
        to_return = {'delta_vals':delta_vals, 'delta_err':delta_err,
                'num_iter':1*self._num_iter, 'frac_err':frac_err,
                'error':self.error, 'exp_err':self._exp_err}
        if get_cos:
            model_cosine = self.calc_model_cosine()
            to_return.update({'model_cosine':model_cosine})
        return to_return