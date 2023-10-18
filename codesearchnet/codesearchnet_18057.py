def update_select_J(self, blk):
        """
        Updates J only for certain parameters, described by the boolean
        mask blk.
        """
        self.update_function(self.param_vals)
        params = np.array(self.param_names)[blk].tolist()
        blk_J = -self.state.gradmodel(params=params, inds=self._inds, flat=False)
        self.J[blk] = blk_J
        #Then we also need to update JTJ:
        self.JTJ = np.dot(self.J, self.J.T)
        if np.any(np.isnan(self.J)) or np.any(np.isnan(self.JTJ)):
            raise FloatingPointError('J, JTJ have nans.')