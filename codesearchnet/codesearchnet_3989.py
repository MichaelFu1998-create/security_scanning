def predict(self, data, graph=None, nruns=6, njobs=None, gpus=0, verbose=None,
                plot=False, plot_generated_pair=False, return_list_results=False):
        """Execute SAM on a dataset given a skeleton or not.

        Args:
            data (pandas.DataFrame): Observational data for estimation of causal relationships by SAM
            skeleton (numpy.ndarray): A priori knowledge about the causal relationships as an adjacency matrix.
                      Can be fed either directed or undirected links.
            nruns (int): Number of runs to be made for causal estimation.
                   Recommended: >=12 for optimal performance.
            njobs (int): Numbers of jobs to be run in Parallel.
                   Recommended: 1 if no GPU available, 2*number of GPUs else.
            gpus (int): Number of available GPUs for the algorithm.
            verbose (bool): verbose mode
            plot (bool): Plot losses interactively. Not recommended if nruns>1
            plot_generated_pair (bool): plots a generated pair interactively.  Not recommended if nruns>1
        Returns:
            networkx.DiGraph: Graph estimated by SAM, where A[i,j] is the term
            of the ith variable for the jth generator.
        """
        verbose, njobs = SETTINGS.get_default(('verbose', verbose), ('nb_jobs', njobs))
        if njobs != 1:
            list_out = Parallel(n_jobs=njobs)(delayed(run_SAM)(data,
                                                               skeleton=graph,
                                                               lr_gen=self.lr, lr_disc=self.dlr,
                                                               regul_param=self.l1, nh=self.nh, dnh=self.dnh,
                                                               gpu=bool(gpus), train_epochs=self.train,
                                                               test_epochs=self.test, batch_size=self.batchsize,
                                                               plot=plot, verbose=verbose, gpu_no=idx % max(gpus, 1))
                                              for idx in range(nruns))
        else:
            list_out = [run_SAM(data, skeleton=graph,
                                lr_gen=self.lr, lr_disc=self.dlr,
                                regul_param=self.l1, nh=self.nh, dnh=self.dnh,
                                gpu=bool(gpus), train_epochs=self.train,
                                test_epochs=self.test, batch_size=self.batchsize,
                                plot=plot, verbose=verbose, gpu_no=0)
                        for idx in range(nruns)]
        if return_list_results:
            return list_out
        else:
            W = list_out[0]
            for w in list_out[1:]:
                W += w
            W /= nruns
        return nx.relabel_nodes(nx.DiGraph(W), {idx: i for idx, i in enumerate(data.columns)})