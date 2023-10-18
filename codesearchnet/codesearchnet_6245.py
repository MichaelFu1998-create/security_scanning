def _is_redundant(self, matrix, cutoff=None):
        """Identify rdeundant rows in a matrix that can be removed."""

        cutoff = 1.0 - self.feasibility_tol

        # Avoid zero variances
        extra_col = matrix[:, 0] + 1

        # Avoid zero rows being correlated with constant rows
        extra_col[matrix.sum(axis=1) == 0] = 2
        corr = np.corrcoef(np.c_[matrix, extra_col])
        corr = np.tril(corr, -1)

        return (np.abs(corr) > cutoff).any(axis=1)