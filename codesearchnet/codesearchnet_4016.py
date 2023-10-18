def orient_directed_graph(self, data, graph):
        """Run the algorithm on a directed_graph.

        Args:
            data (pandas.DataFrame): DataFrame containing the data
            graph (networkx.DiGraph): Skeleton of the graph to orient

        Returns:
            networkx.DiGraph: Solution on the given skeleton.

        .. warning::
           The algorithm is ran on the skeleton of the given graph.

        """
        warnings.warn("The algorithm is ran on the skeleton of the given graph.")
        return self.orient_undirected_graph(data, nx.Graph(graph))