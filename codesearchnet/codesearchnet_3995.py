def anm_score(self, x, y):
        """Compute the fitness score of the ANM model in the x->y direction.

        Args:
            a (numpy.ndarray): Variable seen as cause
            b (numpy.ndarray): Variable seen as effect

        Returns:
            float: ANM fit score
        """
        gp = GaussianProcessRegressor().fit(x, y)
        y_predict = gp.predict(x)
        indepscore = normalized_hsic(y_predict - y, x)

        return indepscore