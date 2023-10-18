def _inference(self, start, lbview, quiet=False):
        """ 
        Inference sends slices of jobs to the parallel engines for computing
        and collects the results into the output hdf5 array as they finish. 
        """

        ## an iterator to distribute sampled quartets in chunks
        gen = xrange(self.checkpoint.arr, self.params.nquartets, self._chunksize)
        njobs = sum(1 for _ in gen)
        jobiter = iter(gen)
        LOGGER.info("chunksize: %s, start: %s, total: %s, njobs: %s", \
            self._chunksize, self.checkpoint.arr, self.params.nquartets, njobs)

        ## if bootstrap create an output array for results unless we are 
        ## restarting an existing boot, then use the one already present
        key = "b{}".format(self.checkpoint.boots)
        with h5py.File(self.database.output, 'r+') as out:
            if key not in out["qboots"].keys():
                out["qboots"].create_dataset(key, 
                                            (self.params.nquartets, 4), 
                                            dtype=np.uint32, 
                                            chunks=(self._chunksize, 4))

        ## initial progress bar
        elapsed = datetime.timedelta(seconds=int(time.time()-start))
        if not self.checkpoint.boots:
            printstr = " initial tree | {} | "
            if not quiet:
                progressbar(1, 0, printstr.format(elapsed), spacer="")
                
        else:
            printstr = " boot {:<7} | {} | "
            if not quiet:
                progressbar(self.params.nboots, self.checkpoint.boots, 
                    printstr.format(self.checkpoint.boots, elapsed), spacer="")

        ## submit all jobs to be distributed across nodes
        res = {}
        for _ in xrange(njobs):
            ## get chunk of quartet samples and send to a worker engine
            qidx = jobiter.next()
            LOGGER.info('submitting chunk: %s', qidx)
            #res[qidx] = lbview.apply(nworker, *[self, qidx, TESTS])
            with h5py.File(self.database.input, 'r') as inh5:
                smps = inh5["samples"][qidx:qidx+self._chunksize]
                res[qidx] = lbview.apply(nworker, *[self, smps, TESTS])

        ## keep adding jobs until the jobiter is empty
        done = 0
        while 1:
            ## check for finished jobs
            curkeys = res.keys()
            finished = [i.ready() for i in res.values()]

            ## remove finished and submit new jobs
            if any(finished):
                for ikey in curkeys:
                    if res[ikey].ready():
                        if res[ikey].successful():
                            ## track finished
                            done += 1
                            ## insert results into hdf5 data base
                            results = res[ikey].get(0)
                            LOGGER.info("%s", results[1])
                            self._insert_to_array(ikey, results) #, bidx)
                            ## purge memory of the old one
                            del res[ikey]
                        else:
                            ## print error if something went wrong
                            raise IPyradWarningExit(""" error in 'inference'\n{}
                                """.format(res[ikey].exception()))

                    ## submit new jobs
                    try:
                        ## send chunk off to be worked on
                        qidx = jobiter.next()
                        with h5py.File(self.database.input, 'r') as inh5:
                            smps = inh5["samples"][qidx:qidx+self._chunksize]
                        res[qidx] = lbview.apply(nworker, *[self, smps, TESTS])

                    ## if no more jobs then just wait until these are done
                    except StopIteration:
                        continue
            else:
                time.sleep(0.01)

            ## print progress unless bootstrapping, diff progbar for that.
            elapsed = datetime.timedelta(seconds=int(time.time()-start))
            if not self.checkpoint.boots:
                if not quiet:
                    progressbar(njobs, done, printstr.format(elapsed), spacer="")
            else:
                if not quiet:
                    progressbar(self.params.nboots, self.checkpoint.boots, 
                        printstr.format(self.checkpoint.boots, elapsed), 
                        spacer="")

            ## done is counted on finish, so this means we're done
            if njobs == done:
                break

        ## dump quartets to a file
        self._dump_qmc()

        ## send to qmc
        if not self.checkpoint.boots:
            self._run_qmc(0)
        else:
            self._run_qmc(1)            

        ## reset the checkpoint_arr
        self.checkpoint.arr = 0