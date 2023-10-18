def _store_equal_samples(self, ncpus):
        """ 
        sample quartets evenly across splits of the starting tree, and fills
        in remaining samples with random quartet samples. Uses a hash dict to 
        not sample the same quartet twice, so for very large trees this can 
        take a few minutes to find millions of possible quartet samples. 
        """
        
        ## choose chunker for h5 arr
        breaks = 2
        if self.params.nquartets < 5000:
            breaks = 1
        if self.params.nquartets > 100000:
            breaks = 4
        if self.params.nquartets > 500000:
            breaks = 8

        self._chunksize = (self.params.nquartets // (breaks * ncpus) + \
                         (self.params.nquartets % (breaks * ncpus)))
        LOGGER.info("nquarts = %s, chunk = %s", self.params.nquartets, self._chunksize)

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

        ## get starting tree, unroot, randomly resolve, ladderize
        tre = ete3.Tree(self.files.guidetreefile, format=0)
        #tre = toytree.tree(self.files.guidetreefile, format=0)
        tre.tree.unroot()
        tre.tree.resolve_polytomy(recursive=True)
        tre.tree.ladderize()

        ## randomly sample all splits of tree and convert tip names to indices
        splits = [([self.samples.index(z.name) for z in i], 
                   [self.samples.index(z.name) for z in j]) \
                   for (i, j) in tre.get_edges()]
    
        ## only keep internal splits (no single tips edges)
        ## this seemed to cause problems with unsampled tips
        splits = [i for i in splits if all([len(j) > 1 for j in i])]

        ## turn each into an iterable split sampler
        ## if the nquartets for that split is small, then sample all of them
        ## if it is big, then make it a random sampler from that split
        qiters = []

        ## how many min quartets are we gonna sample from each split?
        squarts = self.params.nquartets // len(splits)

        ## how many iterators can be sampled to saturation?
        nsaturation = 0

        for split in splits:
            ## if small number at this split then sample all possible sets
            ## we will exhaust this quickly and then switch to random for 
            ## the larger splits.
            if n_choose_k(len(split[0]), 2) * n_choose_k(len(split[1]), 2) < squarts*2:
                qiter = (i+j for (i, j) in itertools.product(
                            itertools.combinations(split[0], 2), 
                            itertools.combinations(split[1], 2)))
                nsaturation += 1

            ## else create random sampler across that split, this is slower
            ## because it can propose the same split repeatedly and so we 
            ## have to check it against the 'sampled' set.
            else:
                qiter = (random_product(split[0], split[1]) for _ \
                         in xrange(self.params.nquartets))
                nsaturation += 1

            ## store all iterators into a list
            qiters.append(qiter)

        #for split in splits:
        #    print(split)

        ## make qiters infinitely cycling
        qiters = itertools.cycle(qiters)
        cycler = itertools.cycle(range(len(splits)))

        ## store visiting quartets
        sampled = set()

        ## iterate over qiters sampling from each, if one runs out, keep 
        ## sampling from remaining qiters. Keep going until samples is filled
        with h5py.File(self.database.input, 'a') as io5:
            ## create data sets
            io5.create_dataset("samples", 
                               (self.params.nquartets, 4), 
                               dtype=np.uint16, 
                               chunks=(self._chunksize, 4),
                               compression='gzip')

            ## fill chunksize at a time for efficiency
            i = 0
            empty = set()
            edge_targeted = 0
            random_target = 0

            ## keep filling quartets until nquartets are sampled
            while i < self.params.nquartets:
                qdat = []
                ## keep filling this chunk until its full
                while len(qdat) < self._chunksize:
                    ## grab the next iterator
                    qiter = qiters.next()
                    cycle = cycler.next()

                    ## sample from iterator
                    try:
                        qrtsamp = qiter.next()
                        if tuple(qrtsamp) not in sampled:
                            qdat.append(qrtsamp)
                            sampled.add(qrtsamp)
                            edge_targeted += 1
                        #else:
                        #    print('repeat')
                        
                    ## unless iterator is empty, then skip it
                    except StopIteration:
                        empty.add(cycle)

                    ## break when all edge samplers are empty
                    if len(empty) == nsaturation:
                        break

                ## if array is not full then add random samples
                while len(qdat) < self._chunksize:
                    qrtsamp = random_combination(range(len(self.samples)), 4)
                    if tuple(qrtsamp) not in sampled:
                        qdat.append(qrtsamp)
                        sampled.add(qrtsamp)
                        random_target += 1

                ## stick chunk into h5 array
                dat = np.array(qdat, dtype=np.uint16)
                io5["samples"][i:i+self._chunksize] = dat[:io5["samples"].shape[0] - i]
                i += self._chunksize

            print("  equal sampling: {} edge quartets, {} random quartets "\
                  .format(edge_targeted, random_target))