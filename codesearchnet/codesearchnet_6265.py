def sample(self, n, fluxes=True):
        """Generate a set of samples.

        This is the basic sampling function for all hit-and-run samplers.

        Paramters
        ---------
        n : int
            The minimum number of samples that are generated at once
            (see Notes).
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

        If the number of processes is larger than one, computation is split
        across as the CPUs of your machine. This may shorten computation time.
        However, there is also overhead in setting up parallel computation so
        we recommend to calculate large numbers of samples at once
        (`n` > 1000).

        """

        if self.processes > 1:
            n_process = np.ceil(n / self.processes).astype(int)
            n = n_process * self.processes

            # The cast to list is weird but not doing it gives recursion
            # limit errors, something weird going on with multiprocessing
            args = list(zip(
                [n_process] * self.processes, range(self.processes)))

            # No with statement or starmap here since Python 2.x
            # does not support it :(
            mp = Pool(self.processes, initializer=mp_init, initargs=(self,))
            results = mp.map(_sample_chain, args, chunksize=1)
            mp.close()
            mp.join()

            chains = np.vstack([r[1] for r in results])
            self.retries += sum(r[0] for r in results)
        else:
            mp_init(self)
            results = _sample_chain((n, 0))
            chains = results[1]

        # Update the global center
        self.center = (self.n_samples * self.center +
                       np.atleast_2d(chains).sum(0)) / (self.n_samples + n)
        self.n_samples += n

        if fluxes:
            names = [r.id for r in self.model.reactions]

            return pandas.DataFrame(
                chains[:, self.fwd_idx] - chains[:, self.rev_idx],
                columns=names)
        else:
            names = [v.name for v in self.model.variables]

            return pandas.DataFrame(chains, columns=names)