def _run2(self):
        """Workhorse for do_run_2"""
        if self.check_update_J():
            self.update_J()
        else:
            if self.check_Broyden_J():
                self.update_Broyden_J()
            if self.check_update_eig_J():
                self.update_eig_J()

        #0. Find _last_residuals, _last_error, etc:
        _last_residuals = self.calc_residuals().copy()
        _last_error = 1*self.error
        _last_vals = self.param_vals.copy()

        #1. Calculate 2 possible steps
        delta_params_1 = self.find_LM_updates(self.calc_grad(),
                do_correct_damping=False)
        self.decrease_damping()
        delta_params_2 = self.find_LM_updates(self.calc_grad(),
                do_correct_damping=False)
        self.decrease_damping(undo_decrease=True)

        #2. Check which step is best:
        er1 = self.update_function(self.param_vals + delta_params_1)
        er2 = self.update_function(self.param_vals + delta_params_2)

        triplet = (self.error, er1, er2)
        best_step = find_best_step(triplet)
        if best_step == 0:
            #Both bad steps, put back & increase damping:
            _ = self.update_function(self.param_vals.copy())
            grad = self.calc_grad()
            CLOG.debug('Bad step, increasing damping')
            CLOG.debug('%f\t%f\t%f' % triplet)
            for _try in range(self._max_inner_loop):
                self.increase_damping()
                delta_vals = self.find_LM_updates(grad)
                er_new = self.update_function(self.param_vals + delta_vals)
                good_step = er_new < self.error
                if good_step:
                    #Update params, error, break:
                    self.update_param_vals(delta_vals, incremental=True)
                    self.error = er_new
                    CLOG.debug('Sufficiently increased damping')
                    CLOG.debug('%f\t%f' % (triplet[0], self.error))
                    break
            else: #for-break-else
                #Throw a warning, put back the parameters
                CLOG.warn('Stuck!')
                self.error = self.update_function(self.param_vals.copy())

        elif best_step == 1:
            #er1 <= er2:
            good_step = True
            CLOG.debug('Good step, same damping')
            CLOG.debug('%f\t%f\t%f' % triplet)
            #Update to er1 params:
            er1_1 = self.update_function(self.param_vals + delta_params_1)
            if np.abs(er1_1 - er1) > 1e-6:
                raise RuntimeError('Function updates are not exact.')
            self.update_param_vals(delta_params_1, incremental=True)
            self.error = er1

        elif best_step == 2:
            #er2 < er1:
            good_step = True
            self.error = er2
            CLOG.debug('Good step, decreasing damping')
            CLOG.debug('%f\t%f\t%f' % triplet)
            #-we're already at the correct parameters
            self.update_param_vals(delta_params_2, incremental=True)
            self.decrease_damping()

        #3. Run with current J, damping; update what we need to::
        if good_step:
            self._last_residuals = _last_residuals
            self._last_error = _last_error
            self._last_vals = _last_vals
            self.error
            self.do_internal_run(initial_count=1)