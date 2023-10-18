def train(self):
        """
        Train model with transformed data
        """
        for i, model in enumerate(self.models):
            N = [int(i * len(self.y)) for i in self.lc_range]
            for n in N:
                X = self.X[:n]
                y = self.y[:n]
                e = Experiment(X, y, model.estimator, self.scores,
                               self.validation_method)
                e.log_folder = self.log_folder
                e.train()