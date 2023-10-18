def create_graph_from_data(self, data, **kwargs):
        """Apply causal discovery on observational data using CCDr.

        Args:
            data (pandas.DataFrame): DataFrame containing the data

        Returns:
            networkx.DiGraph: Solution given by the CCDR algorithm.
        """
        # Building setup w/ arguments.
        self.arguments['{VERBOSE}'] = str(self.verbose).upper()
        results = self._run_ccdr(data, verbose=self.verbose)
        return nx.relabel_nodes(nx.DiGraph(results),
                                {idx: i for idx, i in enumerate(data.columns)})