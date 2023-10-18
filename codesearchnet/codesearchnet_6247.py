def batch(self, batch_size, batch_num, fluxes=True):
        """Create a batch generator.

        This is useful to generate n batches of m samples each.

        Parameters
        ----------
        batch_size : int
            The number of samples contained in each batch (m).
        batch_num : int
            The number of batches in the generator (n).
        fluxes : boolean
            Whether to return fluxes or the internal solver variables. If set
            to False will return a variable for each forward and backward flux
            as well as all additional variables you might have defined in the
            model.

        Yields
        ------
        pandas.DataFrame
            A DataFrame with dimensions (batch_size x n_r) containing
            a valid flux sample for a total of n_r reactions (or variables if
            fluxes=False) in each row.

        """

        for i in range(batch_num):
            yield self.sample(batch_size, fluxes=fluxes)