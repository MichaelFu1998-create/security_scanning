def sample(self, n, fluxes=True):
        """Generate a set of samples.

        This is the basic sampling function for all hit-and-run samplers.

        Parameters
        ----------
        n : int
            The number of samples that are generated at once.
        fluxes : boolean
            Whether to return fluxes or the internal solver variables. If set
            to False will return a variable for each forward and backward flux
            as well as all additional variables you might have defined in the
            model.

        Returns
        -------
        numpy.matrix
            Returns a matrix with `n` rows, each containing a flux sample.

        Notes
        -----
        Performance of this function linearly depends on the number
        of reactions in your model and the thinning factor.

        """

        samples = np.zeros((n, self.warmup.shape[1]))

        for i in range(1, self.thinning * n + 1):
            self.__single_iteration()

            if i % self.thinning == 0:
                samples[i//self.thinning - 1, ] = self.prev

        if fluxes:
            names = [r.id for r in self.model.reactions]

            return pandas.DataFrame(
                samples[:, self.fwd_idx] - samples[:, self.rev_idx],
                columns=names)
        else:
            names = [v.name for v in self.model.variables]

            return pandas.DataFrame(samples, columns=names)