def fit(self):
        """
        Fits the model with random restarts.
        :return:
        """
        self.model.optimize_restarts(num_restarts=self.num_restarts, verbose=False)