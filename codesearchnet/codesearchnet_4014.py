def orient_graph(self, df_data, graph, nb_runs=6, printout=None, **kwargs):
        """Orient an undirected graph using the pairwise method defined by the subclass.

        The pairwise method is ran on every undirected edge.

        Args:
            df_data (pandas.DataFrame): Data
            umg (networkx.Graph): Graph to orient
            nb_runs (int): number of times to rerun for each pair (bootstrap)
            printout (str): (optional) Path to file where to save temporary results

        Returns:
            networkx.DiGraph: a directed graph, which might contain cycles

        .. warning:
           Requirement : Name of the nodes in the graph correspond to name of
           the variables in df_data
        """
        if type(graph) == nx.DiGraph:
            edges = [a for a in list(graph.edges()) if (a[1], a[0]) in list(graph.edges())]
            oriented_edges = [a for a in list(graph.edges()) if (a[1], a[0]) not in list(graph.edges())]
            for a in edges:
                if (a[1], a[0]) in list(graph.edges()):
                    edges.remove(a)
            output = nx.DiGraph()
            for i in oriented_edges:
                output.add_edge(*i)

        elif type(graph) == nx.Graph:
            edges = list(graph.edges())
            output = nx.DiGraph()

        else:
            raise TypeError("Data type not understood.")

        res = []

        for idx, (a, b) in enumerate(edges):
            weight = self.predict_proba(
                df_data[a].values.reshape((-1, 1)), df_data[b].values.reshape((-1, 1)), idx=idx,
                nb_runs=nb_runs, **kwargs)
            if weight > 0:  # a causes b
                output.add_edge(a, b, weight=weight)
            else:
                output.add_edge(b, a, weight=abs(weight))
            if printout is not None:
                res.append([str(a) + '-' + str(b), weight])
                DataFrame(res, columns=['SampleID', 'Predictions']).to_csv(
                    printout, index=False)

        for node in list(df_data.columns.values):
            if node not in output.nodes():
                output.add_node(node)

        return output