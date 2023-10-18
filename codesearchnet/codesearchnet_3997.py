def create_graph_from_data(self, data, **kwargs):
        """Run the PC algorithm.

        Args:
            data (pandas.DataFrame): DataFrame containing the data

        Returns:
            networkx.DiGraph: Solution given by PC on the given data.
       """
        # Building setup w/ arguments.
        self.arguments['{CITEST}'] = self.dir_CI_test[self.CI_test]
        self.arguments['{METHOD_INDEP}'] = self.dir_method_indep[self.method_indep]
        self.arguments['{DIRECTED}'] = 'TRUE'
        self.arguments['{ALPHA}'] = str(self.alpha)
        self.arguments['{NJOBS}'] = str(self.nb_jobs)
        self.arguments['{VERBOSE}'] = str(self.verbose).upper()

        results = self._run_pc(data, verbose=self.verbose)

        return nx.relabel_nodes(nx.DiGraph(results),
                                {idx: i for idx, i in enumerate(data.columns)})