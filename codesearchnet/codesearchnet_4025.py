def mechanism(self, x):
        """Mechanism function."""
        self.nb_step += 1
        x = np.reshape(x, (x.shape[0], 1))

        if(self.nb_step < 5):
            cov = computeGaussKernel(x)
            mean = np.zeros((1, self.points))[0, :]
            y = np.random.multivariate_normal(mean, cov)
        elif(self.nb_step == 5):
            cov = computeGaussKernel(x)
            mean = np.zeros((1, self.points))[0, :]
            y = np.random.multivariate_normal(mean, cov)
            self.gpr = GaussianProcessRegressor()
            self.gpr.fit(x, y)
            y = self.gpr.predict(x)
        else:
            y = self.gpr.predict(x)

        return y