def get_best_candidate(self):
        """
        Returns
        ----------
        best_candidate : the best candidate hyper-parameters as defined by
        """
        # TODO make this best mean response
        self.incumbent = self.surrogate.Y.max()

        # Objective function
        def z(x):
            # TODO make spread of points around x and take mean value.
            x = x.copy().reshape(-1, self.n_dims)
            y_mean, y_var = self.surrogate.predict(x)
            af = self._acquisition_function(y_mean=y_mean, y_var=y_var)
            # TODO make -1 dependent on flag in inputs for either max or minimization
            return (-1) * af

        # Optimization loop
        af_values = []
        af_args = []

        for i in range(self.n_iter):
            init = self._get_random_point()
            res = minimize(z, init, bounds=self.n_dims * [(0., 1.)],
                           options={'maxiter': int(self.max_iter), 'disp': 0})
            af_args.append(res.x)
            af_values.append(res.fun)

        # Choose the best
        af_values = np.array(af_values).flatten()
        af_args = np.array(af_args)
        best_index = int(np.argmin(af_values))
        best_candidate = af_args[best_index]
        return best_candidate