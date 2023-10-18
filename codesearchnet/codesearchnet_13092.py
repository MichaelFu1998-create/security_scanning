def run(self, force=False, quiet=False, ipyclient=None):
        """
        Parameters
        ----------
        force (bool):
            Overwrite existing results for object with the same name
            and workdir as this one.
        verbose (int):
            0=primt nothing; 1=print progress bars; 2=print pringress
            bars and cluster information.
        ipyclient (ipyparallel.Client object):
            A connected ipyclient object. If ipcluster instance is 
            not running on the default profile then ...
        """

        ## force overwrite needs to clear out the HDF5 database
        if force:
            self._refresh()

        ## print nquartet statement
        if not quiet:
            print("inferring {} quartet tree sets".format(self.params.nquartets))

        ## wrap the run in a try statement to ensure we properly shutdown
        ## and cleanup on exit or interrupt. 
        inst = None
        try:
            ## find and connect to an ipcluster instance given the information
            ## in the _ipcluster dictionary if a connected client was not given.
            if not ipyclient:
                args = self._ipcluster.items() + [("spacer", "")]
                ipyclient = ip.core.parallel.get_client(**dict(args))

            ## print the cluster connection information
            if not quiet:
                ip.cluster_info(ipyclient)

            ## store ipyclient engine pids to the dict so we can 
            ## hard-interrupt them later if assembly is interrupted. 
            ## Only stores pids of engines that aren't busy at this moment, 
            ## otherwise it would block here while waiting to find their pids.
            self._ipcluster["pids"] = {}
            for eid in ipyclient.ids:
                engine = ipyclient[eid]
                if not engine.outstanding:
                    pid = engine.apply(os.getpid).get()
                    self._ipcluster["pids"][eid] = pid            

            ## fill the input array with quartets to sample --------------------
            start = time.time()
            if (not self.checkpoint.boots) and (not self.trees.tree):
                self._store_N_samples(start, ipyclient, quiet=quiet)

            ## calculate invariants for the full seqarray ----------------------
            start = time.time()            
            if not self.trees.tree:
                self._inference(start, ipyclient, quiet=quiet)
            else:
                if not quiet:
                    print("initial tree already inferred")

            ## calculate invariants for each bootstrap rep ----------------------
            start = time.time()
            if self.params.nboots:
                if self.checkpoint.boots: #<= self.params.nboots:
                    if not quiet:
                        print("{} bootstrap trees already inferred"\
                              .format(self.checkpoint.boots))

                while self.checkpoint.boots < self.params.nboots:
                    ## resample the bootseq array
                    if self.files.mapfile:
                        self._sample_bootseq_array_map()
                    else:
                        self._sample_bootseq_array()

                    ## start boot inference 
                    self.checkpoint.boots += 1
                    self._inference(start, ipyclient, quiet=quiet)

            ## write output stats -----------------------------------------------
            #self.files.stats = os.path.join(self.dirs, self.name+"_stats.txt")
            start = time.time()
            self._compute_stats(start, ipyclient, quiet=quiet)

        ## handle exceptions so they will be raised after we clean up below
        except KeyboardInterrupt as inst:
            print("\nKeyboard Interrupt by user. Cleaning up...")

        except IPyradWarningExit as inst:
            print("\nError encountered: {}".format(inst))

        except Exception as inst:
            print("\nUnknown exception encountered: {}".format(inst))

        ## close client when done or interrupted
        finally:
            try:
                ## save the Assembly
                self._save()                
                
                ## can't close client if it was never open
                if ipyclient:

                    ## send SIGINT (2) to all engines
                    ipyclient.abort()
                    time.sleep(1)
                    for engine_id, pid in self._ipcluster["pids"].items():
                        if ipyclient.queue_status()[engine_id]["tasks"]:
                            os.kill(pid, 2)
                        time.sleep(0.25)
                    
                    ## if CLI, stop jobs and shutdown
                    if 'ipyrad-cli' in self._ipcluster["cluster_id"]:
                        ipyclient.shutdown(hub=True, block=False)
                        ipyclient.close()
                    else:
                        if not ipyclient.outstanding:
                            ipyclient.purge_everything()
                        else:
                            ## nanny: kill everything, something bad happened
                            ipyclient.shutdown(hub=True, block=False)
                            ipyclient.close()
                            print("\nwarning: ipcluster shutdown and must be restarted")
                
                ## reraise the error now that we're cleaned up
                #if inst:
                #    raise inst

            ## if exception during shutdown then we really screwed up
            except Exception as inst2:
                print("warning: error during shutdown:\n{}".format(inst2))