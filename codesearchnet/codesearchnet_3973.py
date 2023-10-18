def fit(self, x, y):
        """Train the model.

        Args:
            x_tr (pd.DataFrame): CEPC format dataframe containing the pairs
            y_tr (pd.DataFrame or np.ndarray): labels associated to the pairs
        """
        train = np.vstack((np.array([self.featurize_row(row.iloc[0],
                                                        row.iloc[1]) for idx, row in x.iterrows()]),
                           np.array([self.featurize_row(row.iloc[1],
                                                        row.iloc[0]) for idx, row in x.iterrows()])))
        labels = np.vstack((y, -y)).ravel()
        verbose = 1 if self.verbose else 0
        self.clf = CLF(verbose=verbose,
                       min_samples_leaf=self.L,
                       n_estimators=self.E,
                       max_depth=self.max_depth,
                       n_jobs=self.n_jobs).fit(train, labels)