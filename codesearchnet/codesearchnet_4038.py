def predict_proba(self, a, b, nb_runs=6, nb_jobs=None, gpu=None,
                      idx=0, verbose=None, ttest_threshold=0.01,
                      nb_max_runs=16, train_epochs=1000, test_epochs=1000):
        """Run multiple times GNN to estimate the causal direction.

        Args:
            a (np.ndarray): Variable 1
            b (np.ndarray): Variable 2
            nb_runs (int): number of runs to execute per batch (before testing for significance with t-test).
            nb_jobs (int): number of runs to execute in parallel. (Initialized with ``cdt.SETTINGS.NB_JOBS``)
            gpu (bool): use gpu (Initialized with ``cdt.SETTINGS.GPU``)
            idx (int): (optional) index of the pair, for printing purposes
            verbose (bool): verbosity (Initialized with ``cdt.SETTINGS.verbose``)
            ttest_threshold (float): threshold to stop the boostraps before ``nb_max_runs`` if the difference is significant
            nb_max_runs (int): Max number of bootstraps
            train_epochs (int): Number of epochs during which the model is going to be trained
            test_epochs (int): Number of epochs during which the model is going to be tested

        Returns:
            float: Causal score of the pair (Value : 1 if a->b and -1 if b->a)
        """
        Nb_jobs, verbose, gpu = SETTINGS.get_default(('nb_jobs', nb_jobs), ('verbose', verbose), ('gpu', gpu))
        x = np.stack([a.ravel(), b.ravel()], 1)
        ttest_criterion = TTestCriterion(
            max_iter=nb_max_runs, runs_per_iter=nb_runs, threshold=ttest_threshold)

        AB = []
        BA = []

        while ttest_criterion.loop(AB, BA):
            if nb_jobs != 1:
                result_pair = Parallel(n_jobs=nb_jobs)(delayed(GNN_instance)(
                    x, idx=idx, device='cuda:{}'.format(run % gpu) if gpu else 'cpu',
                    verbose=verbose, train_epochs=train_epochs, test_epochs=test_epochs) for run in range(ttest_criterion.iter, ttest_criterion.iter + nb_runs))
            else:
                result_pair = [GNN_instance(x, idx=idx,
                                            device='cuda:0' if gpu else 'cpu',
                                            verbose=verbose,
                                            train_epochs=train_epochs,
                                            test_epochs=test_epochs)
                               for run in range(ttest_criterion.iter, ttest_criterion.iter + nb_runs)]
            AB.extend([runpair[0] for runpair in result_pair])
            BA.extend([runpair[1] for runpair in result_pair])

        if verbose:
            print("P-value after {} runs : {}".format(ttest_criterion.iter,
                                                      ttest_criterion.p_value))

        score_AB = np.mean(AB)
        score_BA = np.mean(BA)

        return (score_BA - score_AB) / (score_BA + score_AB)