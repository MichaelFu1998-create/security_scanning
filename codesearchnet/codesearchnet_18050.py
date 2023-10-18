def update_select_J(self, blk):
        """
        Updates J only for certain parameters, described by the boolean
        mask `blk`.
        """
        p0 = self.param_vals.copy()
        self.update_function(p0)  #in case things are not put back...
        r0 = self.calc_residuals().copy()
        dl = np.zeros(p0.size, dtype='float')
        blk_J = []
        for i in np.nonzero(blk)[0]:
            dl *= 0; dl[i] = self.eig_dl
            self.update_function(p0 + dl)
            r1 = self.calc_residuals().copy()
            blk_J.append((r1-r0)/self.eig_dl)
        self.J[blk] = np.array(blk_J)
        self.update_function(p0)
        #Then we also need to update JTJ:
        self.JTJ = np.dot(self.J, self.J.T)
        if np.any(np.isnan(self.J)) or np.any(np.isnan(self.JTJ)):
            raise FloatingPointError('J, JTJ have nans.')