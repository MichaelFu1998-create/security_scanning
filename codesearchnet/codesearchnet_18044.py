def update_J(self):
        """Updates J, JTJ, and internal counters."""
        self.calc_J()
        # np.dot(j, j.T) is slightly faster but 2x as much mem
        step = np.ceil(1e-2 * self.J.shape[1]).astype('int')  # 1% more mem...
        self.JTJ = low_mem_sq(self.J, step=step)
        #copies still, since J is not C -ordered but a slice of j_e...
        #doing self.J.copy() works but takes 2x as much ram..
        self._fresh_JTJ = True
        self._J_update_counter = 0
        if np.any(np.isnan(self.JTJ)):
            raise FloatingPointError('J, JTJ have nans.')
        #Update self._exp_err
        self._exp_err = self.error - self.find_expected_error(delta_params='perfect')