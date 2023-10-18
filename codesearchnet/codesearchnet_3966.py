def create_graph_from_data(self, data):
        """Use CGNN to create a graph from scratch. All the possible structures
        are tested, which leads to a super exponential complexity. It would be
        preferable to start from a graph skeleton for large graphs.

        Args:
            data (pandas.DataFrame): Observational data on which causal
               discovery has to be performed.
        Returns:
            networkx.DiGraph: Solution given by CGNN.

        """
        warnings.warn("An exhaustive search of the causal structure of CGNN without"
                      " skeleton is super-exponential in the number of variables.")

        # Building all possible candidates:
        nb_vars = len(list(data.columns))
        data = scale(data.values).astype('float32')

        candidates = [np.reshape(np.array(i), (nb_vars, nb_vars)) for i in itertools.product([0, 1], repeat=nb_vars*nb_vars)
                      if (np.trace(np.reshape(np.array(i), (nb_vars, nb_vars))) == 0
                          and nx.is_directed_acyclic_graph(nx.DiGraph(np.reshape(np.array(i), (nb_vars, nb_vars)))))]

        warnings.warn("A total of {} graphs will be evaluated.".format(len(candidates)))
        scores = [parallel_graph_evaluation(data, i, nh=self.nh, nb_runs=self.nb_runs, gpu=self.gpu,
                                            nb_jobs=self.nb_jobs, lr=self.lr, train_epochs=self.train_epochs,
                                            test_epochs=self.test_epochs, verbose=self.verbose) for i in candidates]
        final_candidate = candidates[scores.index(min(scores))]
        output = np.zeros(final_candidate.shape)

        # Retrieve the confidence score on each edge.
        for (i, j), x in np.ndenumerate(final_candidate):
            if x > 0:
                cand = final_candidate
                cand[i, j] = 0
                output[i, j] = min(scores) - scores[candidates.index(cand)]

        return nx.DiGraph(candidates[output],
                          {idx: i for idx, i in enumerate(data.columns)})