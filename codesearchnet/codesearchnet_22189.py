def X(self):
        """
        The :math:`X` weighted properly by the errors from *y_error*
        """
        if self._X is None:
            X = _copy.deepcopy(self.X_unweighted)
            # print 'X shape is {}'.format(X.shape)
            for i, el in enumerate(X):
                X[i, :] = el/self.y_error[i]
            # print 'New X shape is {}'.format(X.shape)
            self._X = X
        return self._X