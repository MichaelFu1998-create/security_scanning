def calc_accel_correction(self, damped_JTJ, delta0):
        """
        Geodesic acceleration correction to the LM step.

        Parameters
        ----------
            damped_JTJ : numpy.ndarray
                The damped JTJ used to calculate the initial step.
            delta0 : numpy.ndarray
                The initial LM step.

        Returns
        -------
            corr : numpy.ndarray
                The correction to the original LM step.
        """
        #Get the derivative:
        _ = self.update_function(self.param_vals)
        rm0 = self.calc_residuals().copy()
        _ = self.update_function(self.param_vals + delta0)
        rm1 = self.calc_residuals().copy()
        _ = self.update_function(self.param_vals - delta0)
        rm2 = self.calc_residuals().copy()
        der2 = (rm2 + rm1 - 2*rm0)

        corr, res, rank, s = np.linalg.lstsq(damped_JTJ, np.dot(self.J, der2),
                rcond=self.min_eigval)
        corr *= -0.5
        return corr