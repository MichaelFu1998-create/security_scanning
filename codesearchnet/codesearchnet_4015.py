def orient_undirected_graph(self, data, graph):
        """Run the algorithm on an undirected graph.

        Args:
            data (pandas.DataFrame): DataFrame containing the data
            graph (networkx.Graph): Skeleton of the graph to orient

        Returns:
            networkx.DiGraph: Solution on the given skeleton.

        """
        # Building setup w/ arguments.
        self.arguments['{VERBOSE}'] = str(self.verbose).upper()
        self.arguments['{SCORE}'] = self.score
        self.arguments['{BETA}'] = str(self.beta)
        self.arguments['{OPTIM}'] = str(self.optim).upper()
        self.arguments['{ALPHA}'] = str(self.alpha)

        whitelist = DataFrame(list(nx.edges(graph)), columns=["from", "to"])
        blacklist = DataFrame(list(nx.edges(nx.DiGraph(DataFrame(-nx.adj_matrix(graph, weight=None).to_dense() + 1,
                                                                 columns=list(graph.nodes()),
                                                                 index=list(graph.nodes()))))), columns=["from", "to"])
        results = self._run_bnlearn(data, whitelist=whitelist,
                                   blacklist=blacklist, verbose=self.verbose)

        return nx.relabel_nodes(nx.DiGraph(results),
                                {idx: i for idx, i in enumerate(data.columns)})