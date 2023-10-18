def find_expected_error(self, delta_params='calc', adjust=True):
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
        expected_error = super(LMGlobals, self).find_expected_error(
                delta_params=delta_params)
        if adjust:
            #adjust for num_pix
            derr = (expected_error - self.error) * (self.state.residuals.size /
                    float(self.num_pix))
            expected_error = self.error + derr
        return expected_error