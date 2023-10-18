def resample_factor(self, factor):
        """Resample to a new regular grid.


        Parameters
        ----------
        factor : float
            The number of grid cells are scaled with `factor` in each
            dimension, i.e., ``factor * N_i`` cells along each
            dimension i.


        Returns
        -------
        Grid


        See Also
        --------
        resample

        """
        # new number of edges N' = (N-1)*f + 1
        newlengths = [(N - 1) * float(factor) + 1 for N in self._len_edges()]
        edges = [numpy.linspace(start, stop, num=int(N), endpoint=True)
                 for (start, stop, N) in
                 zip(self._min_edges(), self._max_edges(), newlengths)]
        return self.resample(edges)