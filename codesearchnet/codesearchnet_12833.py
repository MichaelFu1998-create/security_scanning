def write_nexus_files(self, force=False, quiet=False):
        """
        Write nexus files to {workdir}/{name}/[0-N].nex, If the directory already
        exists an exception will be raised unless you use the force flag which 
        will remove all files in the directory. 

        Parameters:
        -----------
        force (bool):
            If True then all files in {workdir}/{name}/*.nex* will be removed. 

        """

        ## clear existing files 
        existing = glob.glob(os.path.join(self.workdir, self.name, "*.nex"))
        if any(existing):
            if force:
                for rfile in existing:
                    os.remove(rfile)
            else:
                path = os.path.join(self.workdir, self.name)
                raise IPyradWarningExit(EXISTING_NEX_FILES.format(path))

        ## parse the loci or alleles file
        with open(self.files.data) as infile:
            loci = iter(infile.read().strip().split("|\n"))

        ## use entered samples or parse them from the file
        if not self.samples:
            with open(self.files.data) as infile:
                samples = set((i.split()[0] for i in infile.readlines() \
                               if "//" not in i))
        else:
            samples = set(self.samples)

        ## keep track of how many loci pass filtering
        totn = len(samples)
        nloci = 0

        ## this set is just used for matching, then we randomly
        ## subsample for real within the locus so it varies 
        if self._alleles:
            msamples = {i+rbin() for i in samples}
        else:
            msamples = samples

        ## write subsampled set of loci
        for loc in loci:
            ## get names and seqs from locus
            dat = loc.split("\n")[:-1]
            try:
                names = [i.split()[0] for i in dat]
                snames = set(names)
                seqs = np.array([list(i.split()[1]) for i in dat])
            except IndexError:
                print(ALLELESBUGFIXED)
                continue

            ## check name matches
            if len(snames.intersection(msamples)) == totn:

                ## prune sample names if alleles. Done here so it is randomly
                ## different in every locus which allele is selected from 
                ## each sample (e.g., 0 or 1)
                if self._alleles:
                    _samples = [i+rbin() for i in samples]
                else:
                    _samples = samples

                ## re-order seqs to be in set order
                seqsamp = seqs[[names.index(tax) for tax in _samples]]

                ## resolve ambiguities randomly if .loci file otherwise
                ## sample one of the alleles if .alleles file.
                if not self._alleles:
                    seqsamp = _resolveambig(seqsamp)

                ## find parsimony informative sites
                if _count_PIS(seqsamp, self.params.minsnps):
                    ## keep the locus
                    nloci += 1

                    ## remove empty columns given this sampling
                    copied = seqsamp.copy()
                    copied[copied == "-"] == "N"
                    rmcol = np.all(copied == "N", axis=0)
                    seqsamp = seqsamp[:, ~rmcol]

                    ## write nexus file
                    if self._alleles:
                        ## trim off the allele number
                        samps = [i.rsplit("_", 1)[0] for i in _samples]
                        mdict = dict(zip(samps, [i.tostring() for i in seqsamp]))
                    else:
                        mdict = dict(zip(_samples, [i.tostring() for i in seqsamp]))
                    self._write_nex(mdict, nloci)

                    ## quit early if using maxloci
                    if nloci == self.params.maxloci: 
                        break


        ## print data size
        if not quiet:
            path = os.path.join(self.workdir, self.name)
            path = path.replace(os.path.expanduser("~"), "~")
            print("wrote {} nexus files to {}".format(nloci, path))