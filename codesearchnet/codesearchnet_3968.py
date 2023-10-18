def orient_undirected_graph(self, data, umg, alg='HC'):
        """Orient the undirected graph using GNN and apply CGNN to improve the graph.

        Args:
            data (pandas.DataFrame): Observational data on which causal
               discovery has to be performed.
            umg (nx.Graph): Graph that provides the skeleton, on which the GNN
               then the CGNN algorithm will be applied.
            alg (str): Exploration heuristic to use, among ["HC", "HCr",
               "tabu", "EHC"]
        Returns:
            networkx.DiGraph: Solution given by CGNN.
       
        .. note::
           GNN (``cdt.causality.pairwise.GNN``) is first used to orient the
           undirected graph and output a DAG before applying CGNN.
        """
        warnings.warn("The pairwise GNN model is computed on each edge of the UMG "
                      "to initialize the model and start CGNN with a DAG")
        gnn = GNN(nh=self.nh, lr=self.lr)

        og = gnn.orient_graph(data, umg, nb_runs=self.nb_runs, nb_max_runs=self.nb_runs,
                              nb_jobs=self.nb_jobs, train_epochs=self.train_epochs,
                              test_epochs=self.test_epochs, verbose=self.verbose, gpu=self.gpu)  # Pairwise method
        # print(nx.adj_matrix(og).todense().shape)
        # print(list(og.edges()))
        dag = dagify_min_edge(og)
        # print(nx.adj_matrix(dag).todense().shape)

        return self.orient_directed_graph(data, dag, alg=alg)