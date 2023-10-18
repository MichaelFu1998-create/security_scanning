def _store_N_samples(self, start, ipyclient, quiet=False):
        """ 
        Find all quartets of samples and store in a large array
        A chunk size is assigned for sampling from the array of quartets
        based on the number of cpus available. This should be relatively 
        large so that we don't spend a lot of time doing I/O, but small 
        enough that jobs finish often for checkpointing.
        """

        breaks = 2
        if self.params.nquartets < 5000:
            breaks = 1
        if self.params.nquartets > 100000:
            breaks = 8
        if self.params.nquartets > 500000:
            breaks = 16
        if self.params.nquartets > 5000000:
            breaks = 32

        ## chunk up the data
        ncpus = len(ipyclient)    
        self._chunksize = (self.params.nquartets // (breaks * ncpus) \
                        + (self.params.nquartets % (breaks * ncpus)))

        ## create h5 OUT empty arrays
        ## 'quartets' stores the inferred quartet relationship (1 x 4)
        ## This can get huge, so we need to choose the dtype wisely. 
        ## the values are simply the index of the taxa, so uint16 is good.
        with h5py.File(self.database.output, 'w') as io5:
            io5.create_dataset("quartets", 
                               (self.params.nquartets, 4), 
                               dtype=np.uint16, 
                               chunks=(self._chunksize, 4))
            ## group for bootstrap invariant matrices ((16, 16), uint32)
            ## these store the actual matrix counts. dtype uint32 can store
            ## up to 4294967295. More than enough. uint16 max is 65535.
            ## the 0 boot is the original seqarray.
            io5.create_group("invariants")

        ## append to h5 IN array (which has the seqarray, bootsarr, maparr)
        ## and fill it with all of the quartet sets we will ever sample.
        ## the samplign method will vary depending on whether this is random, 
        ## all, or equal splits (in a separate but similar function). 
        with h5py.File(self.database.input, 'a') as io5:
            try:
                io5.create_dataset("quartets", 
                               (self.params.nquartets, 4), 
                               dtype=np.uint16, 
                               chunks=(self._chunksize, 4),
                               compression='gzip')
            except RuntimeError:
                raise IPyradWarningExit(
                    "database file already exists for this analysis, "
                  + "you must run with the force flag to overwrite")
            
        ## submit store job to write into self.database.input
        if self.params.method == "all":
            async = ipyclient[0].apply(store_all, self)
        elif self.params.method == "random":
            async = ipyclient[0].apply(store_random, self)
        elif self.params.method == "equal":
            async = ipyclient[0].apply(store_equal, self) 

        ## progress bar 
        printstr = "generating q-sets | {} | "
        prog = 0        
        while 1:
            elapsed = datetime.timedelta(seconds=int(time.time()-start))
            if not quiet:
                if async.stdout:
                    prog = int(async.stdout.strip().split()[-1])
                progressbar(self.params.nquartets, prog,
                            printstr.format(elapsed), spacer="")
            if not async.ready():
                time.sleep(0.1)
            else:
                break

        if not async.successful():
            raise IPyradWarningExit(async.result())
        if not quiet:
            print("")