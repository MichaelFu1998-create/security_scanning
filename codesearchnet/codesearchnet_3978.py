def predict(self, df_data, threshold=0.05, **kwargs):
        """Predict the skeleton of the graph from raw data.

        Returns iteratively the feature selection algorithm on each node.

        Args:
            df_data (pandas.DataFrame): data to construct a graph from
            threshold (float): cutoff value for feature selection scores
            kwargs (dict): additional arguments for algorithms

        Returns:
            networkx.Graph: predicted skeleton of the graph.
        """
        nb_jobs = kwargs.get("nb_jobs", SETTINGS.NB_JOBS)
        list_nodes = list(df_data.columns.values)
        if nb_jobs != 1:
            result_feature_selection = Parallel(n_jobs=nb_jobs)(delayed(self.run_feature_selection)
                                                                (df_data, node, idx, **kwargs)
                                                                for idx, node in enumerate(list_nodes))
        else:
            result_feature_selection = [self.run_feature_selection(df_data, node, idx, **kwargs) for idx, node in enumerate(list_nodes)]
        for idx, i in enumerate(result_feature_selection):
            try:
                i.insert(idx, 0)
            except AttributeError:  # if results are numpy arrays
                result_feature_selection[idx] = np.insert(i, idx, 0)
        matrix_results = np.array(result_feature_selection)
        matrix_results *= matrix_results.transpose()
        np.fill_diagonal(matrix_results, 0)
        matrix_results /= 2

        graph = nx.Graph()

        for (i, j), x in np.ndenumerate(matrix_results):
            if matrix_results[i, j] > threshold:
                graph.add_edge(list_nodes[i], list_nodes[j],
                               weight=matrix_results[i, j])
        for node in list_nodes:
            if node not in graph.nodes():
                graph.add_node(node)
        return graph