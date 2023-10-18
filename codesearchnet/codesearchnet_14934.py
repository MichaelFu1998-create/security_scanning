def fit(self, X, y=None):
        """Learning is to find the inverse matrix for X and calculate the threshold.

        Parameters
        ----------
        X : array-like or sparse matrix, shape (n_samples, n_features)
            The input samples. Use ``dtype=np.float32`` for maximum
            efficiency.
        y : array-like, shape = [n_samples] or [n_samples, n_outputs]
            The target values (real numbers in regression).

        Returns
        -------
        self : object
        """
        # Check that X have correct shape
        X = check_array(X)
        self.inverse_influence_matrix = self.__make_inverse_matrix(X)
        if self.threshold == 'auto':
            self.threshold_value = 3 * (1 + X.shape[1]) / X.shape[0]
        elif self.threshold == 'cv':
            if y is None:
                raise ValueError("Y must be specified to find the optimal threshold.")
            y = check_array(y, accept_sparse='csc', ensure_2d=False, dtype=None)
            self.threshold_value = 0
            score = 0
            Y_pred, Y_true, AD = [], [], []
            cv = KFold(n_splits=5, random_state=1, shuffle=True)
            for train_index, test_index in cv.split(X):
                x_train = safe_indexing(X, train_index)
                x_test = safe_indexing(X, test_index)
                y_train = safe_indexing(y, train_index)
                y_test = safe_indexing(y, test_index)
                if self.reg_model is None:
                    reg_model = RandomForestRegressor(n_estimators=500, random_state=1).fit(x_train, y_train)
                else:
                    reg_model = clone(self.reg_model).fit(x_train, y_train)
                Y_pred.append(reg_model.predict(x_test))
                Y_true.append(y_test)
                ad_model = self.__make_inverse_matrix(x_train)
                AD.append(self.__find_leverages(x_test, ad_model))
            AD_ = unique(hstack(AD))
            for z in AD_:
                AD_new = hstack(AD) <= z
                if self.score == 'ba_ad':
                    val = balanced_accuracy_score_with_ad(Y_true=hstack(Y_true), Y_pred=hstack(Y_pred), AD=AD_new)
                elif self.score == 'rmse_ad':
                    val = rmse_score_with_ad(Y_true=hstack(Y_true), Y_pred=hstack(Y_pred), AD=AD_new)
                if val >= score:
                    score = val
                    self.threshold_value = z
        else:
            self.threshold_value = self.threshold
        return self