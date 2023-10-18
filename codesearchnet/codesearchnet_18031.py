def _run1(self):
        """workhorse for do_run_1"""
        if self.check_update_J():
            self.update_J()
        else:
            if self.check_Broyden_J():
                self.update_Broyden_J()
            if self.check_update_eig_J():
                self.update_eig_J()

        #1. Assuming that J starts updated:
        delta_vals = self.find_LM_updates(self.calc_grad())

        #2. Increase damping until we get a good step:
        er1 = self.update_function(self.param_vals + delta_vals)
        good_step = (find_best_step([self.error, er1]) == 1)
        if not good_step:
            er0 = self.update_function(self.param_vals)
            if np.abs(er0 -self.error)/er0 > 1e-7:
                raise RuntimeError('Function updates are not exact.')
            CLOG.debug('Bad step, increasing damping')
            CLOG.debug('\t\t%f\t%f' % (self.error, er1))
            grad = self.calc_grad()
            for _try in range(self._max_inner_loop):
                self.increase_damping()
                delta_vals = self.find_LM_updates(grad)
                er1 = self.update_function(self.param_vals + delta_vals)
                good_step = (find_best_step([self.error, er1]) == 1)
                if good_step:
                    break
            else:
                er0 = self.update_function(self.param_vals)
                CLOG.warn('Stuck!')
                if np.abs(er0 -self.error)/er0 > 1e-7:
                    raise RuntimeError('Function updates are not exact.')

        #state is updated, now params:
        if good_step:
            self._last_error = self.error
            self.error = er1
            CLOG.debug('Good step\t%f\t%f' % (self._last_error, self.error))
            self.update_param_vals(delta_vals, incremental=True)
            self.decrease_damping()