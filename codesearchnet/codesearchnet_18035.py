def find_LM_updates(self, grad, do_correct_damping=True, subblock=None):
        """
        Calculates LM updates, with or without the acceleration correction.

        Parameters
        ----------
            grad : numpy.ndarray
                The gradient of the model cost.
            do_correct_damping : Bool, optional
                If `self.use_accel`, then set to True to correct damping
                if the acceleration correction is too big. Default is True
                Does nothing is `self.use_accel` is False
            subblock : slice, numpy.ndarray, or None, optional
                Set to a slice or a valide numpy.ndarray to use only a
                certain subset of the parameters. Default is None, i.e.
                use all the parameters.

        Returns
        -------
            delta : numpy.ndarray
                The Levenberg-Marquadt step, relative to the old
                parameters. Size is always self.param_vals.size.
        """
        if subblock is not None:
            if (subblock.sum() == 0) or (subblock.size == 0):
                CLOG.fatal('Empty subblock in find_LM_updates')
                raise ValueError('Empty sub-block')
            j = self.J[subblock]
            JTJ = np.dot(j, j.T)
            damped_JTJ = self._calc_damped_jtj(JTJ, subblock=subblock)
            grad = grad[subblock]  #select the subblock of the grad
        else:
            damped_JTJ = self._calc_damped_jtj(self.JTJ, subblock=subblock)

        delta = self._calc_lm_step(damped_JTJ, grad, subblock=subblock)

        if self.use_accel:
            accel_correction = self.calc_accel_correction(damped_JTJ, delta)
            nrm_d0 = np.sqrt(np.sum(delta**2))
            nrm_corr = np.sqrt(np.sum(accel_correction**2))
            CLOG.debug('|correction| / |LM step|\t%e' % (nrm_corr/nrm_d0))
            if nrm_corr/nrm_d0 < self.max_accel_correction:
                delta += accel_correction
            elif do_correct_damping:
                CLOG.debug('Untrustworthy step! Increasing damping...')
                self.increase_damping()
                damped_JTJ = self._calc_damped_jtj(self.JTJ, subblock=subblock)
                delta = self._calc_lm_step(damped_JTJ, grad, subblock=subblock)

        if np.any(np.isnan(delta)):
            CLOG.fatal('Calculated steps have nans!?')
            raise FloatingPointError('Calculated steps have nans!?')
        return delta