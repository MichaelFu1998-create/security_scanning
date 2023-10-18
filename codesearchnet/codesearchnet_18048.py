def update_eig_J(self):
        """Execute an eigen update of J"""
        CLOG.debug('Eigen update.')
        vls, vcs = np.linalg.eigh(self.JTJ)
        res0 = self.calc_residuals()
        for a in range(min([self.num_eig_dirs, vls.size])):
            #1. Finding stiff directions
            stif_dir = vcs[-(a+1)] #already normalized

            #2. Evaluating derivative along that direction, we'll use dl=5e-4:
            dl = self.eig_dl #1e-5
            _ = self.update_function(self.param_vals + dl*stif_dir)
            res1 = self.calc_residuals()

            #3. Updating
            grad_stif = (res1-res0)/dl
            self._rank_1_J_update(stif_dir, grad_stif)

        self.JTJ = np.dot(self.J, self.J.T)
        #Putting the parameters back:
        _ = self.update_function(self.param_vals)