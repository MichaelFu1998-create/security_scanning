def find_expected_error(self, delta_params='calc'):
        """
        Returns the error expected after an update if the model were linear.

        Parameters
        ----------
            delta_params : {numpy.ndarray, 'calc', or 'perfect'}, optional
                The relative change in parameters. If 'calc', uses update
                calculated from the current damping, J, etc; if 'perfect',
                uses the update calculated with zero damping.

        Returns
        -------
            numpy.float64
                The expected error after the update with `delta_params`
        """
        grad = self.calc_grad()
        if list(delta_params) in [list('calc'), list('perfect')]:
            jtj = (self.JTJ if delta_params == 'perfect' else
                    self._calc_damped_jtj(self.JTJ))
            delta_params = self._calc_lm_step(jtj, self.calc_grad())
        #If the model were linear, then the cost would be quadratic,
        #with Hessian 2*`self.JTJ` and gradient `grad`
        expected_error = (self.error + np.dot(grad, delta_params) +
                np.dot(np.dot(self.JTJ, delta_params), delta_params))
        return expected_error