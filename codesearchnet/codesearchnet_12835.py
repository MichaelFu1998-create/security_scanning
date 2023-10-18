def _write_nex(self, mdict, nlocus):
        """ 
        function that takes a dictionary mapping names to sequences, 
        and a locus number, and writes it as a NEXUS file with a mrbayes 
        analysis block given a set of mcmc arguments.
        """

        ## create matrix as a string
        max_name_len = max([len(i) for i in mdict])
        namestring = "{:<" + str(max_name_len+1) + "} {}\n"
        matrix = ""
        for i in mdict.items():
            matrix += namestring.format(i[0], i[1])

        ## ensure dir
        minidir = os.path.realpath(os.path.join(self.workdir, self.name))
        if not os.path.exists(minidir):
            os.makedirs(minidir)

        ## write nexus block
        handle = os.path.join(minidir, "{}.nex".format(nlocus))
        with open(handle, 'w') as outnex:
            outnex.write(NEXBLOCK.format(**{
                "ntax": len(mdict), 
                "nchar": len(mdict.values()[0]), 
                "matrix": matrix,
                "ngen": self.params.mb_mcmc_ngen, 
                "sfreq": self.params.mb_mcmc_sample_freq, 
                "burnin": self.params.mb_mcmc_burnin, 
                }))