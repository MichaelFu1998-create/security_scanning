def do_internal_run(self, initial_count=0, subblock=None, update_derr=True):
        """
        Takes more steps without calculating J again.

        Given a fixed damping, J, JTJ, iterates calculating steps, with
        optional Broyden or eigendirection updates. Iterates either until
        a bad step is taken or for self.run_length times.
        Called internally by do_run_2() but is also useful on its own.

        Parameters
        ----------
            initial_count : Int, optional
                The initial count of the run. Default is 0. Increasing from
                0 effectively temporarily decreases run_length.
            subblock : None or np.ndarray of bools, optional
                If not None, a boolean mask which determines which sub-
                block of parameters to run over. Default is None, i.e.
                all the parameters.
            update_derr : Bool, optional
                Set to False to not update the variable that determines
                delta_err, preventing premature termination through errtol.

        Notes
        -----
        It might be good to do something similar to update_derr with the
        parameter values, but this is trickier because of Broyden updates
        and _fresh_J.
        """
        self._inner_run_counter = initial_count; good_step = True
        n_good_steps = 0
        CLOG.debug('Running...')

        _last_residuals = self.calc_residuals().copy()
        while ((self._inner_run_counter < self.run_length) & good_step &
                (not self.check_terminate())):
            #1. Checking if we update J
            if self.check_Broyden_J() and self._inner_run_counter != 0:
                self.update_Broyden_J()
            if self.check_update_eig_J() and self._inner_run_counter != 0:
                self.update_eig_J()

            #2. Getting parameters, error
            er0 = 1*self.error
            delta_vals = self.find_LM_updates(self.calc_grad(),
                    do_correct_damping=False, subblock=subblock)
            er1 = self.update_function(self.param_vals + delta_vals)
            good_step = er1 < er0

            if good_step:
                n_good_steps += 1
                CLOG.debug('%f\t%f' % (er0, er1))
                #Updating:
                self.update_param_vals(delta_vals, incremental=True)
                self._last_residuals = _last_residuals.copy()
                if update_derr:
                    self._last_error = er0
                self.error = er1

                _last_residuals = self.calc_residuals().copy()
            else:
                er0_0 = self.update_function(self.param_vals)
                CLOG.debug('Bad step!')
                if np.abs(er0 - er0_0) > 1e-6:
                    raise RuntimeError('Function updates are not exact.')

            self._inner_run_counter += 1
        return n_good_steps