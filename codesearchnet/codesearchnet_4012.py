def predict(self, x, *args, **kwargs):
        """Generic predict method, chooses which subfunction to use for a more
        suited.

        Depending on the type of `x` and of `*args`, this function process to execute
        different functions in the priority order:

        1. If ``args[0]`` is a ``networkx.(Di)Graph``, then ``self.orient_graph`` is executed.
        2. If ``args[0]`` exists, then ``self.predict_proba`` is executed.
        3. If ``x`` is a ``pandas.DataFrame``, then ``self.predict_dataset`` is executed.
        4. If ``x`` is a ``pandas.Series``, then ``self.predict_proba`` is executed.

        Args:
            x (numpy.array or pandas.DataFrame or pandas.Series): First variable or dataset.
            args (numpy.array or networkx.Graph): graph or second variable.

        Returns:
            pandas.Dataframe or networkx.Digraph: predictions output
        """
        if len(args) > 0:
            if type(args[0]) == nx.Graph or type(args[0]) == nx.DiGraph:
                return self.orient_graph(x, *args, **kwargs)
            else:
                return self.predict_proba(x, *args, **kwargs)
        elif type(x) == DataFrame:
            return self.predict_dataset(x, *args, **kwargs)
        elif type(x) == Series:
            return self.predict_proba(x.iloc[0], x.iloc[1], *args, **kwargs)