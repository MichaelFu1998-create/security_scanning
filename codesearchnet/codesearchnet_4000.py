def predict(self, data, alpha=0.01, max_iter=2000, **kwargs):
        """ Predict the graph skeleton.

        Args:
            data (pandas.DataFrame): observational data
            alpha (float): regularization parameter
            max_iter (int): maximum number of iterations

        Returns:
            networkx.Graph: Graph skeleton
        """
        edge_model = GraphLasso(alpha=alpha, max_iter=max_iter)
        edge_model.fit(data.values)

        return nx.relabel_nodes(nx.DiGraph(edge_model.get_precision()),
                                {idx: i for idx, i in enumerate(data.columns)})