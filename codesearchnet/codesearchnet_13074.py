def store_equal(self):
    """
    Takes a tetrad class object and populates array with random 
    quartets sampled equally among splits of the tree so that 
    deep splits are not overrepresented relative to rare splits, 
    like those near the tips. 
    """

    with h5py.File(self.database.input, 'a') as io5:
        fillsets = io5["quartets"]

        ## require guidetree
        if not os.path.exists(self.files.tree):
            raise IPyradWarningExit(
                "To use sampling method 'equal' requires a guidetree")
        tre = ete3.Tree(self.files.tree)
        tre.unroot()
        tre.resolve_polytomy(recursive=True)

        ## randomly sample internals splits
        splits = [([self.samples.index(z.name) for z in i],
                   [self.samples.index(z.name) for z in j]) \
                   for (i, j) in tre.get_edges()]

        ## only keep internal splits, not single tip edges
        splits = [i for i in splits if all([len(j) > 1 for j in i])]

        ## how many min quartets shoudl be equally sampled from each split
        squarts = self.params.nquartets // len(splits)

        ## keep track of how many iterators are saturable.
        saturable = 0

        ## turn each into an iterable split sampler
        ## if the nquartets for that split is small, then sample all, 
        ## if it is big then make it a random sampler for that split.
        qiters = []

        ## iterate over splits sampling quartets evenly
        for idx, split in enumerate(splits):
            ## if small number at this split then sample all possible sets
            ## we will exhaust this quickly and then switch to random for 
            ## the larger splits.
            total = n_choose_k(len(split[0]), 2) * n_choose_k(len(split[1]), 2)
            if total < squarts*2:
                qiter = (i+j for (i, j) in itertools.product(
                            itertools.combinations(split[0], 2), 
                            itertools.combinations(split[1], 2)))
                saturable += 1

            ## else create random sampler across that split, this is slower
            ## because it can propose the same split repeatedly and so we 
            ## have to check it against the 'sampled' set.
            else:
                qiter = (random_product(split[0], split[1]) for _ \
                         in xrange(self.params.nquartets))

            ## store all iterators into a list
            qiters.append((idx, qiter))

        ## create infinite cycler of qiters
        qitercycle = itertools.cycle(qiters)

        ## store visited quartets
        sampled = set()

        ## fill chunksize at a time
        i = 0
        empty = set()
        edge_targeted = 0
        random_targeted = 0

        ## keep filling quartets until nquartets are sampled.
        while i < self.params.nquartets:
            ## grab the next iterator
            cycle, qiter = qitercycle.next()

            ## sample from iterators, store sorted set.
            try:
                qrtsamp = tuple(sorted(qiter.next()))
                if qrtsamp not in sampled:
                    sampled.add(qrtsamp)
                    edge_targeted += 1
                    i += 1
                    ## print progress bar update to engine stdout
                    if not i % self._chunksize:
                        print(min(i, self.params.nquartets))                    

            except StopIteration:
                empty.add(cycle)
                if len(empty) == saturable:
                    break


        ## if array is not full then add random samples
        while i <= self.params.nquartets:
            newset = tuple(sorted(np.random.choice(
                range(len(self.samples)), 4, replace=False)))
            if newset not in sampled:
                sampled.add(newset)
                random_targeted += 1
                i += 1
                ## print progress bar update to engine stdout
                if not i % self._chunksize:
                    print(min(i, self.params.nquartets))

        ## store into database
        print(self.params.nquartets)
        fillsets[:] = np.array(tuple(sampled))
        del sampled