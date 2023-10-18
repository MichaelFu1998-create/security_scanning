def store_random(self):
    """
    Populate array with random quartets sampled from a generator.
    Holding all sets in memory might take a lot, but holding a very
    large list of random numbers for which ones to sample will fit 
    into memory for most reasonable sized sets. So we'll load a 
    list of random numbers in the range of the length of total 
    sets that can be generated, then only keep sets from the set 
    generator if they are in the int list. I did several tests to 
    check that random pairs are as likely as 0 & 1 to come up together
    in a random quartet set. 
    """

    with h5py.File(self.database.input, 'a') as io5:
        fillsets = io5["quartets"]

        ## set generators
        qiter = itertools.combinations(xrange(len(self.samples)), 4)
        rand = np.arange(0, n_choose_k(len(self.samples), 4))
        np.random.shuffle(rand)
        rslice = rand[:self.params.nquartets]
        rss = np.sort(rslice)
        riter = iter(rss)
        del rand, rslice

        ## print progress update 1 to the engine stdout
        print(self._chunksize)

        ## set to store
        rando = riter.next()
        tmpr = np.zeros((self.params.nquartets, 4), dtype=np.uint16)
        tidx = 0
        while 1:
            try:
                for i, j in enumerate(qiter):
                    if i == rando:
                        tmpr[tidx] = j
                        tidx += 1
                        rando = riter.next()

                    ## print progress bar update to engine stdout
                    if not i % self._chunksize:
                        print(min(i, self.params.nquartets))

            except StopIteration:
                break
        ## store into database
        fillsets[:] = tmpr
        del tmpr