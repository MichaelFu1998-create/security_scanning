def set_interpolation_coefficients(self):
        """
        computes the coefficients for the single polynomials of the spline.
        """

        left_boundary_slope = 0
        right_boundary_slope = 0

        if isinstance(self.boundary_condition, tuple):
            left_boundary_slope = self.boundary_condition[0]
            right_boundary_slope = self.boundary_condition[1]
        elif self.boundary_condition is None:
            pass
        else:
            msg = 'The given object {} of type {} is not a valid condition ' \
                  'for the border'.format(self.boundary_condition, type(self.boundary_condition))
            raise ValueError(msg)

        # getting the values such that we get a continuous second derivative
        # by solving a system of linear equations

        # setup the matrix
        n = len(self.x_list)
        mat = numpy.zeros((n, n))
        b = numpy.zeros((n, 1))
        x = self.x_list
        y = self.y_list

        if n > 2:
            for i in range(1, n - 1):
                mat[i, i - 1] = 1.0 / (x[i] - x[i - 1])
                mat[i, i + 1] = 1.0 / (x[i + 1] - x[i])
                mat[i, i] = 2 * (mat[i, i - 1] + mat[i, i + 1])

                b[i, 0] = 3 * ((y[i] - y[i - 1]) / (x[i] - x[i - 1]) ** 2
                               + (y[i + 1] - y[i]) / (x[i + 1] - x[i]) ** 2)
        elif n < 2:
            raise ValueError('too less points for interpolation')

        if self.boundary_condition is None:  # not a knot
            mat[0, 0] = 1.0 / (x[1] - x[0]) ** 2
            mat[0, 2] = -1.0 / (x[2] - x[1]) ** 2
            mat[0, 1] = mat[0, 0] + mat[0, 2]

            b[0, 0] = 2.0 * ((y[1] - y[0]) / (x[1] - x[0]) ** 3
                             - (y[2] - y[1]) / (x[2] - x[1]) ** 3)

            mat[n - 1, n - 3] = 1.0 / (x[n - 2] - x[n - 3]) ** 2
            mat[n - 1, n - 1] = -1.0 / (x[n - 1] - x[n - 2]) ** 2
            mat[n - 1, n - 2] = mat[n - 1, n - 3] + mat[n - 1, n - 1]

            b[n - 1, 0] = 2.0 * ((y[n - 2] - y[n - 3]) / (x[n - 2] - x[n - 3]) ** 3
                                 - (y[n - 1] - y[n - 2]) / (x[n - 1] - x[n - 2]) ** 3)
        else:
            mat[0, 0] = 2.0 / (x[1] - x[0])
            mat[0, 1] = 1.0 / (x[1] - x[0])

            b[0, 0] = 3 * (y[1] - y[0]) / (x[1] - x[0]) ** 2 - 0.5 * left_boundary_slope

            mat[n - 1, n - 2] = 1.0 / (x[n - 1] - x[n - 2])
            mat[n - 1, n - 1] = 2.0 / (x[n - 1] - x[n - 2])

            b[n - 1, 0] = 3 * (y[n - 1] - y[n - 2]) / (x[n - 1] - x[n - 2]) ** 2 + 0.5 * right_boundary_slope

        k = numpy.linalg.solve(mat, b)

        for i in range(1, n):
            c1 = k[i - 1, 0] * (x[i] - x[i - 1]) - (y[i] - y[i - 1])
            c2 = -k[i, 0] * (x[i] - x[i - 1]) + (y[i] - y[i - 1])
            self.interpolation_coefficients.append([c1, c2])