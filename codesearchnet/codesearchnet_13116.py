def write_structure_files(self, kpop, rep=1):
        """ 
        Prepares input files for running structure. Users typically do not need
        to call this function since it is called internally by .run(). But it
        is optionally available here in case users wish to generate files and 
        run structure separately.
        """

        ## check params
        self.mainparams.numreps = int(self.mainparams.numreps)
        self.mainparams.burnin = int(self.mainparams.burnin)

        ## write tmp files for the job. Rando avoids filename conflict.
        mname = OPJ(self.workdir, "tmp-{}-{}-{}.mainparams.txt".format(self.name, kpop, rep))
        ename = OPJ(self.workdir, "tmp-{}-{}-{}.extraparams.txt".format(self.name, kpop, rep))
        sname = OPJ(self.workdir, "tmp-{}-{}-{}.strfile.txt".format(self.name, kpop, rep))
        tmp_m = open(mname, 'w')
        tmp_e = open(ename, 'w')
        tmp_s = open(sname, 'w')

        ## write params files
        tmp_m.write(self.mainparams._asfile())
        tmp_e.write(self.extraparams._asfile())

        ## subsample SNPs as unlinked if a mapfile is present.
        ## & write pop data to the tmp_s file if present
        assert len(self.popdata) == len(self.labels), \
            "popdata list must be the same length as the number of taxa"

        with open(self.data) as ifile:
            _data = ifile.readlines()
            ## header
            header = np.array([i.strip().split("\t")[:5] for i in _data])
            ## seqdata
            seqdata = np.array([i.strip().split("\t")[5:] for i in _data])

            ## enter popdata into seqfile if present in self
            if any(self.popdata):
                ## set popdata in header
                header[::2, 1] = self.popdata
                header[1::2, 1] = self.popdata
                
                ## set flag to all 1s if user entered popdata but no popflag
                if not any(self.popflag):
                    self.popflag = [1 for i in self.popdata]
                    header[:, 2] = 1
                else:
                    header[::2, 2] = self.popflag
                    header[1::2, 2] = self.popflag

            ## subsample SNPs if mapfile is present
            if isinstance(self.maparr, np.ndarray):
                seqdata = seqdata[:, self._subsample()]
                
            ## write fullstr
            fullstr = np.concatenate([header, seqdata], axis=1)
            np.savetxt(tmp_s, fullstr, delimiter="\t", fmt="%s")

        ## close tmp files
        tmp_m.close()
        tmp_e.close()
        tmp_s.close()
        return mname, ename, sname