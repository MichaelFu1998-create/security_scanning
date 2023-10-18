def calc_model_cosine(self, decimate=None, mode='err'):
        """
        Calculates the cosine of the residuals with the model.

        Parameters
        ----------
            decimate : Int or None, optional
                Decimate the residuals by `decimate` pixels. If None, no
                decimation is used. Valid only with mode='svd'. Default
                is None
            mode : {'svd', 'err'}
                Which mode to use; see Notes section. Default is 'err'.

        Returns
        -------
            abs_cos : numpy.float64
                The absolute value of the model cosine.

        Notes
        -----
        The model cosine is defined in terms of the geometric view of
        curve-fitting, as a model manifold embedded in a high-dimensional
        space. The model cosine is the cosine of the residuals vector
        with its projection on the tangent space: :math:`cos(phi) = |P^T r|/|r|`
        where :math:`P^T` is the projection operator onto the model manifold
        and :math:`r` the residuals. This can be calculated two ways: By
        calculating the projection operator P directly with SVD (mode=`svd`),
        or by using the expected error if the model were linear to calculate
        a model sine first (mode=`err`). Since the SVD of a large matrix is
        slow, mode=`err` is faster.

        `decimate` allows for every nth pixel only to be counted in the
        SVD matrix of J for speed. While this is n x faster, it is
        considerably less accurate, so the default is no decimation.
        """
        #we calculate the model cosine only in the data space of the
        #sampled indices
        if mode == 'err':
            expected_error = self.find_expected_error(delta_params='perfect',
                    adjust=False)
            derr = self.error - expected_error
            residuals_err = lambda r: np.dot(r,r).sum()
            current_partial_error = residuals_err(self.calc_residuals())
            expected_partial_error = current_partial_error - derr
            model_sine_2 = expected_partial_error / current_partial_error
            abs_cos = np.sqrt(1 - model_sine_2)
        else:
            #superclass is fine
            abs_cos = super(self.__class__, self).calc_model_cosine(decimate=
                    decimate, mode=mode)
        return abs_cos