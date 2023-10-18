def predict_undirected_graph(self, data):
        """Build a skeleton using a pairwise independence criterion.

        Args:
            data (pandas.DataFrame): Raw data table

        Returns:
            networkx.Graph: Undirected graph representing the skeleton.
        """
        graph = Graph()

        for idx_i, i in enumerate(data.columns):
            for idx_j, j in enumerate(data.columns[idx_i+1:]):
                score = self.predict(data[i].values, data[j].values)
                if abs(score) > 0.001:
                    graph.add_edge(i, j, weight=score)

        return graph