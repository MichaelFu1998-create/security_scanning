def store_all(self):
    """
    Populate array with all possible quartets. This allows us to 
    sample from the total, and also to continue from a checkpoint
    """

    with h5py.File(self.database.input, 'a') as io5:
        fillsets = io5["quartets"]

        ## generator for all quartet sets
        qiter = itertools.combinations(xrange(len(self.samples)), 4)
        i = 0
        while i < self.params.nquartets:
            ## sample a chunk of the next ordered N set of quartets
            dat = np.array(list(itertools.islice(qiter, self._chunksize)))
            end = min(self.params.nquartets, dat.shape[0]+i)
            fillsets[i:end] = dat[:end-i]
            i += self._chunksize

            ## send progress update to stdout on engine
            print(min(i, self.params.nquartets))