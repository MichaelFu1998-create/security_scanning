def orient_directed_graph(self, data, dag, alg='HC'):
        """Modify and improve a directed acyclic graph solution using CGNN.

        Args:
            data (pandas.DataFrame): Observational data on which causal
               discovery has to be performed.
            dag (nx.DiGraph): Graph that provides the initial solution,
               on which the CGNN algorithm will be applied.
            alg (str): Exploration heuristic to use, among ["HC", "HCr",
               "tabu", "EHC"]
        Returns:
            networkx.DiGraph: Solution given by CGNN.
       
        """
        alg_dic = {'HC': hill_climbing, 'HCr': hill_climbing_with_removal,
                   'tabu': tabu_search, 'EHC': exploratory_hill_climbing}

        return alg_dic[alg](data, dag, nh=self.nh, nb_runs=self.nb_runs, gpu=self.gpu,
                            nb_jobs=self.nb_jobs, lr=self.lr, train_epochs=self.train_epochs,
                            test_epochs=self.test_epochs, verbose=self.verbose)