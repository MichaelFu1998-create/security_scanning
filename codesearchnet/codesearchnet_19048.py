def export_posterior_probability(self, filename, title="Posterior Probability"):
        """
        Writes the posterior probability of read origin

        :param filename: File name for output
        :param title: The title of the posterior probability matrix
        :return: Nothing but the method writes a file in EMASE format (PyTables)
        """
        self.probability.save(h5file=filename, title=title)