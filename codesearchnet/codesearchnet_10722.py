def log_determinant_of_matrix_cholesky(matrix):
        """There are two terms in the inversion's Bayesian likelihood function which require the log determinant of \
        a matrix. These are (Nightingale & Dye 2015, Nightingale, Dye and Massey 2018):

        ln[det(F + H)] = ln[det(curvature_reg_matrix)]
        ln[det(H)]     = ln[det(regularization_matrix)]

        The curvature_reg_matrix is positive-definite, which means the above log determinants can be computed \
        efficiently (compared to using np.det) by using a Cholesky decomposition first and summing the log of each \
        diagonal term.

        Parameters
        -----------
        matrix : ndarray
            The positive-definite matrix the log determinant is computed for.
        """
        try:
            return 2.0 * np.sum(np.log(np.diag(np.linalg.cholesky(matrix))))
        except np.linalg.LinAlgError:
            raise exc.InversionException()