def run(self, force=0, verbose=2, ipyclient=None):
        """ 
        Run quartet inference on a SNP alignment and distribute work
        across an ipyparallel cluster (ipyclient). Unless passed an 
        ipyclient explicitly, it looks for a running ipcluster instance
        running from the defautl ("") profile, and will raise an exception
        if one is not found within a set time limit. If not using the default
        profile then you can set "profile" as an argument to the tetrad object. 
        Parameter settings influencing the run (e.g., nquartets, method) should
        be set on the tetrad Class object itself. 

        Parameters
        ----------
        force (bool):
            Overwrite results for an object with this name if they exist.
        verbose (int):
            0=print nothing, 1=print progress bars, 2=print progress bars and
            print cluster info. 
        ipyclient (ipyparallel.Client object):
            Default is None (use running Default ipcluster instance). To use
            a different ipcluster instance start a Client class object 
            and pass it in as an argument here. 
        """

        ## clear object results and data if force=True
        if force:
            self.refresh()

        ## wrap everything in a try statement so we can ensure that it will
        ## save if interrupted and we will clean up the 
        inst = None
        try:
            ## launch and connect to ipcluster instance if doesn't exist
            if not ipyclient:
                args = self._ipcluster.items() + [("spacer", "")] 
                ipyclient = ip.core.parallel.get_client(**dict(args)) 

            ## print a message about the cluster status
            if verbose == 2:
                ip.cluster_info(ipyclient)

            ## grab 2 engines from each host (2 multi-thread jobs per host)
            ## skips over engines that are busy running something else to avoid
            ## blocking if user is sharing an ipcluster.
            targets = get_targets(ipyclient)
            lbview = ipyclient.load_balanced_view(targets=targets)

            ## store ipyclient pids to the ipcluster instance so we can 
            ## hard-kill them later. 
            self._ipcluster["pids"] = ipyclient[:].apply(os.getpid).get_dict()

            ## get or init quartet sampling ---------------------------
            ## if load=True then chunksize will exist and this will skip
            if not self._chunksize:
                #self.nquartets = n_choose_k(len(self.samples), 4)
                ## store N sampled quartets into the h5 array
                if self.params.method != 'equal':
                    self._store_N_samples(ncpus=len(lbview))
                else:
                    self._store_equal_samples(ncpus=len(lbview))

            ## calculate invariants for the full array ----------------
            start = time.time()            
            if not self.trees.tree:
                if verbose:
                    print("inferring {} induced quartet trees".format(self.params.nquartets))
                self._inference(start, lbview, quiet=verbose == 0)
                if verbose:
                    print("")
            else:
                if verbose:
                    print("initial tree already inferred")

            ## calculate for bootstraps -------------------------------            
            start = time.time()
            if self.params.nboots:
                if self.checkpoint.boots == self.params.nboots:
                    if verbose:
                        print("{} bootstrap trees already inferred".format(self.params.nboots))
                else:
                    while self.checkpoint.boots < self.params.nboots:
                        ## resample bootsstrap seqarray
                        if self.files.mapfile:
                            self._sample_bootseq_array_map()
                        else:
                            self._sample_bootseq_array() 

                        ## start boot inference, (1-indexed !!!)
                        self.checkpoint.boots += 1
                        self._inference(start, lbview, quiet=verbose == 0)
                if verbose:
                    print("")

            ## write outputs with bootstraps ---------------------------
            self.files.stats = os.path.join(self.dirs, self.name+"_stats.txt")
            if not self.kwargs.get("cli"):
                self._compute_tree_stats(ipyclient)
            else:
                self._finalize_stats(ipyclient)


        ## handle exceptions so they will be raised after we clean up below
        except KeyboardInterrupt as inst:
            LOGGER.info("assembly interrupted by user.")
            print("\nKeyboard Interrupt by user. Cleaning up...")

        except IPyradWarningExit as inst:
            LOGGER.info("IPyradWarningExit: %s", inst)
            print(inst)

        except Exception as inst:
            LOGGER.info("caught an unknown exception %s", inst)
            print("\n  Exception found: {}".format(inst))

        ## close client when done or interrupted
        finally:
            try:
                ## save the Assembly
                self._save()                
                
                ## can't close client if it was never open
                if ipyclient:

                    ## send SIGINT (2) to all engines
                    ipyclient.abort()
                    LOGGER.info("what %s", self._ipcluster["pids"])
                    for engine_id, pid in self._ipcluster["pids"].items():
                        LOGGER.info("eid %s", engine_id)
                        LOGGER.info("pid %s", pid)
                        LOGGER.info("queue %s", ipyclient.queue_status()[engine_id]["queue"])
                        if ipyclient.queue_status()[engine_id]["queue"]:
                            LOGGER.info('interrupting engine {} w/ SIGINT to {}'\
                                        .format(engine_id, pid))
                            os.kill(pid, 2)
                    time.sleep(1)

                    ## if CLI, stop jobs and shutdown
                    if 'ipyrad-cli' in self._ipcluster["cluster_id"]:
                        LOGGER.info("  shutting down engines")
                        ipyclient.shutdown(hub=True, block=False)
                        ipyclient.close()
                        LOGGER.info("  finished shutdown")
                    else:
                        if not ipyclient.outstanding:
                            ipyclient.purge_everything()
                        else:
                            ## nanny: kill everything, something bad happened
                            ipyclient.shutdown(hub=True, block=False)
                            ipyclient.close()
                            print("\nwarning: ipcluster shutdown and must be restarted")
                
                ## reraise the error now that we're cleaned up
                if inst:
                    raise inst
            ## if exception is close and save, print and ignore
            except Exception as inst2:
                print("warning: error during shutdown:\n{}".format(inst2))
                LOGGER.error("shutdown warning: %s", inst2)