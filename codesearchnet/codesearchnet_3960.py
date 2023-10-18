def predict(self, df_data, graph=None, **kwargs):
        """Orient a graph using the method defined by the arguments.

        Depending on the type of `graph`, this function process to execute
        different functions:

        1. If ``graph`` is a ``networkx.DiGraph``, then ``self.orient_directed_graph`` is executed.
        2. If ``graph`` is a ``networkx.Graph``, then ``self.orient_undirected_graph`` is executed.
        3. If ``graph`` is a ``None``, then ``self.create_graph_from_data`` is executed.

        Args:
            df_data (pandas.DataFrame): DataFrame containing the observational data.
            graph (networkx.DiGraph or networkx.Graph or None): Prior knowledge on the causal graph.

        .. warning::
           Requirement : Name of the nodes in the graph must correspond to the
           name of the variables in df_data
        """
        if graph is None:
            return self.create_graph_from_data(df_data, **kwargs)
        elif isinstance(graph, nx.DiGraph):
            return self.orient_directed_graph(df_data, graph, **kwargs)
        elif isinstance(graph, nx.Graph):
            return self.orient_undirected_graph(df_data, graph, **kwargs)
        else:
            print('Unknown Graph type')
            raise ValueError