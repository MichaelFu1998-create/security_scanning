def fit(self, X, y=None):
        """Compute the minimum and maximum to be used for later scaling.

        Parameters
        ----------
        X : array-like, shape [n_samples, n_features]
            The data used to compute the per-feature minimum and maximum
            used for later scaling along the features axis.
        """
        X = check_array(X, copy=self.copy,
                        dtype=[np.float64, np.float32, np.float16, np.float128])

        feature_range = self.feature_range
        if feature_range[0] >= feature_range[1]:
            raise ValueError("Minimum of desired feature range must be smaller"
                             " than maximum. Got %s." % str(feature_range))
        if self.fit_feature_range is not None:
            fit_feature_range = self.fit_feature_range
            if fit_feature_range[0] >= fit_feature_range[1]:
                raise ValueError("Minimum of desired (fit) feature range must "
                                 "be smaller than maximum. Got %s."
                                 % str(feature_range))
            if (fit_feature_range[0] < feature_range[0] or
                    fit_feature_range[1] > feature_range[1]):
                raise ValueError("fit_feature_range must be a subset of "
                                 "feature_range. Got %s, fit %s."
                                 % (str(feature_range),
                                    str(fit_feature_range)))
            feature_range = fit_feature_range

        data_min = np.min(X, axis=0)
        data_range = np.max(X, axis=0) - data_min
        # Do not scale constant features
        data_range[data_range == 0.0] = 1.0
        self.scale_ = (feature_range[1] - feature_range[0]) / data_range
        self.min_ = feature_range[0] - data_min * self.scale_
        self.data_range = data_range
        self.data_min = data_min
        return self