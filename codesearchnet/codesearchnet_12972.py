def _store_N_samples(self, ncpus):
        """ 
        Find all quartets of samples and store in a large array
        Create a chunk size for sampling from the array of quartets. 
        This should be relatively large so that we don't spend a lot of time 
        doing I/O, but small enough that jobs finish often for checkpointing.
        """
        breaks = 2
        if self.params.nquartets < 5000:
            breaks = 1
        if self.params.nquartets > 100000:
            breaks = 4
        if self.params.nquartets > 500000:
            breaks = 8

        ## chunk up the data
        self._chunksize = (self.params.nquartets // (breaks * ncpus) + \
                          (self.params.nquartets % (breaks * ncpus)))
        LOGGER.info("nquarts = %s, chunk = %s", self.params.nquartets, self._chunksize)

        ## 'samples' stores the indices of the quartet. 
        ## `quartets` stores the correct quartet in the order (1,2|3,4)
        ## `weights` stores the weight of the quartet in 'quartets'
        ## we gzip this for now, but check later if this has a big speed cost

        ## create h5 OUT empty arrays
        with h5py.File(self.database.output, 'w') as io5:
            io5.create_dataset("quartets", 
                               (self.params.nquartets, 4), 
                               dtype=np.uint16, 
                               chunks=(self._chunksize, 4))
            io5.create_dataset("qstats", 
                               (self.params.nquartets, 4), 
                               dtype=np.uint32, 
                               chunks=(self._chunksize, 4))
            io5.create_group("qboots")


        ## append to h5 IN array (which also has seqarray) and fill it
        with h5py.File(self.database.input, 'a') as io5:
            ## create data sets
            io5.create_dataset("samples", 
                               (self.params.nquartets, 4), 
                               dtype=np.uint16, 
                               chunks=(self._chunksize, 4),
                               compression='gzip')

            ## populate array with all possible quartets. This allows us to 
            ## sample from the total, and also to continue from a checkpoint
            qiter = itertools.combinations(xrange(len(self.samples)), 4)
            i = 0

            ## fill chunksize at a time for efficiency
            while i < self.params.nquartets:
                if self.params.method != "all":
                    ## grab the next random 1000
                    qiter = []
                    while len(qiter) < min(self._chunksize, io5["samples"].shape[0]):
                        qiter.append(
                            random_combination(range(len(self.samples)), 4))
                    dat = np.array(qiter)
                else:
                    ## grab the next ordered chunksize
                    dat = np.array(list(itertools.islice(qiter, self._chunksize)))

                ## store to h5 
                io5["samples"][i:i+self._chunksize] = dat[:io5["samples"].shape[0] - i]
                i += self._chunksize