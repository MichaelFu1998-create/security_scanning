def dist_percentile_threshold(dist_matrix, perc_thr=0.05, k=1):
        """Thresholds a distance matrix and returns the result.

        Parameters
        ----------

        dist_matrix: array_like
        Input array or object that can be converted to an array.

        perc_thr: float in range of [0,100]
        Percentile to compute which must be between 0 and 100 inclusive.

        k: int, optional
        Diagonal above which to zero elements.
        k = 0 (the default) is the main diagonal,
        k < 0 is below it and k > 0 is above.

        Returns
        -------
        array_like

        """
        triu_idx = np.triu_indices(dist_matrix.shape[0], k=k)
        upper = np.zeros_like(dist_matrix)
        upper[triu_idx] = dist_matrix[triu_idx] < np.percentile(dist_matrix[triu_idx], perc_thr)
        return upper