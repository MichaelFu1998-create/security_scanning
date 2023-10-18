def b_fit_score(self, x, y):
        """ Compute the RECI fit score

        Args:
            x (numpy.ndarray): Variable 1
            y (numpy.ndarray): Variable 2

        Returns:
            float: RECI fit score

        """
        x = np.reshape(minmax_scale(x), (-1, 1))
        y = np.reshape(minmax_scale(y), (-1, 1))
        poly = PolynomialFeatures(degree=self.degree)
        poly_x = poly.fit_transform(x)

        poly_x[:,1] = 0
        poly_x[:,2] = 0

        regressor = LinearRegression()
        regressor.fit(poly_x, y)

        y_predict = regressor.predict(poly_x)
        error = mean_squared_error(y_predict, y)

        return error