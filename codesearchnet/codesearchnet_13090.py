def _inference(self, start, ipyclient, quiet):
        """
        Sends slices of quartet sets to parallel engines for computing, 
        enters results into output database, sends finished quartet sets
        to QMC for tree inference, and prints progress bars.
        """

        ## load-balancer for single-threaded execution jobs
        lbview = ipyclient.load_balanced_view()

        ## an iterator that grabs quartet chunk start positions
        jobs = range(self.checkpoint.arr, self.params.nquartets, self._chunksize)

        ## if this is a bootstrap then init a new boot array in the database
        ## max val is 65535 in here if uint16
        bootkey = "boot{}".format(self.checkpoint.boots)
        with h5py.File(self.database.output, 'r+') as io5:
            if bootkey not in io5["invariants"].keys():
                io5["invariants"].create_dataset(
                    bootkey, 
                    (self.params.nquartets, 16, 16),
                    dtype=np.uint16,
                    chunks=(self._chunksize, 16, 16))

        ## start progress bar if new or skip if bootstrapping
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        if self.checkpoint.boots:
            printstr = "bootstrap trees   | {} | "
        else:
            printstr = "initial tree      | {} | "
            if not quiet:
                progressbar(1, 0, printstr.format(elapsed), spacer="")

        ## submit jobs distriuted across the cluster.
        asyncs = {}
        for job in jobs:
            asyncs[job] = lbview.apply(nworker, *(self, job))

        ## wait for jobs to finish, catch results as they return and
        ## enter them into the HDF5 database to keep memory low.
        done = 0
        while 1:
            ## gather finished jobs
            finished = [i for i,j in asyncs.iteritems() if j.ready()]

            ## iterate over finished list
            for key in finished:
                async = asyncs[key]
                if async.successful():
                    ## store result
                    done += 1
                    results = async.result()
                    self._insert_to_array(key, results)
                    ## purge from memory
                    del asyncs[key]
                else:
                    raise IPyradWarningExit(async.result())

            ## progress bar is different if first vs boot tree
            elapsed = datetime.timedelta(seconds=int(time.time()-start))
            if not self.checkpoint.boots:
                if not quiet:
                    progressbar(len(jobs), done, printstr.format(elapsed), spacer="")
            else:
                if not quiet:
                    progressbar(self.params.nboots, self.checkpoint.boots,
                                printstr.format(elapsed), spacer="")

            ## done is counted on finish, so this means we're done
            if len(asyncs) == 0:
                break
            else:
                time.sleep(0.1)

        ## dump quartets into a text file for QMC
        self._dump_qmc()

        ## send to QMC
        if not self.checkpoint.boots:
            self._run_qmc(0)
        else:
            self._run_qmc(1)

        ## reset the checkpoint arr
        self.checkpoint.arr = 0

        ## print spacer if finished first tree or last boot.
        if (not self.checkpoint.boots) and (not quiet):
            print("")

        elif (self.checkpoint.boots == self.params.nboots) and (not quiet):
            print("")