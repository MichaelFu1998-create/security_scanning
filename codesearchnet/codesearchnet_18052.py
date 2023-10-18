def calc_J(self):
        """Updates self.J, returns nothing"""
        del self.J
        self.J = np.zeros([self.param_vals.size, self.data.size])
        dp = np.zeros_like(self.param_vals)
        f0 = self.model.copy()
        for a in range(self.param_vals.size):
            dp *= 0
            dp[a] = self.dl[a]
            f1 = self.func(self.param_vals + dp, *self.func_args, **self.func_kwargs)
            grad_func = (f1 - f0) / dp[a]
            #J = grad(residuals) = -grad(model)
            self.J[a] = -grad_func