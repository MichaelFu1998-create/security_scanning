def _write_ctlfile(self):#, rep=None):
        """ write outfile with any args in argdict """

        ## A string to store ctl info
        ctl = []

        ## write the top header info
        ctl.append("seed = {}".format(self.params.seed))
        ctl.append("seqfile = {}".format(self.seqfile))
        ctl.append("Imapfile = {}".format(self.mapfile))

        path = os.path.realpath(os.path.join(self.workdir, self._name))
        mcmcfile = "{}.mcmc.txt".format(path)
        outfile = "{}.out.txt".format(path)
        if mcmcfile not in self.files.mcmcfiles:
            self.files.mcmcfiles.append(mcmcfile)
        if outfile not in self.files.outfiles:
            self.files.outfiles.append(outfile)

        ctl.append("mcmcfile = {}".format(mcmcfile))
        ctl.append("outfile = {}".format(outfile))

        ## number of loci (checks that seq file exists and parses from there)
        ctl.append("nloci = {}".format(self._nloci))
        ctl.append("usedata = {}".format(self.params.usedata))
        ctl.append("cleandata = {}".format(self.params.cleandata))

        ## infer species tree
        if self.params.infer_sptree:
            ctl.append("speciestree = 1 0.4 0.2 0.1")
        else:
            ctl.append("speciestree = 0")

        ## infer delimitation (with algorithm 1 by default)
        ctl.append("speciesdelimitation = {} {} {}"\
                   .format(self.params.infer_delimit, 
                           self.params.delimit_alg[0],
                           " ".join([str(i) for i in self.params.delimit_alg[1:]]) 
                           )
                   )
        ## get tree values
        nspecies = str(len(self.imap))
        species = " ".join(sorted(self.imap))
        ninds = " ".join([str(len(self.imap[i])) for i in sorted(self.imap)])
        ctl.append(SPECIESTREE.format(nspecies, species, ninds, self.tree.write(format=9)))

        ## priors
        ctl.append("thetaprior = {} {}".format(*self.params.thetaprior))
        ctl.append("tauprior = {} {} {}".format(*self.params.tauprior))

        ## other values, fixed for now
        ctl.append("finetune = 1: {}".format(" ".join([str(i) for i in self.params.finetune])))
        #CTL.append("finetune = 1: 1 0.002 0.01 0.01 0.02 0.005 1.0")
        ctl.append("print = 1 0 0 0")
        ctl.append("burnin = {}".format(self.params.burnin))
        ctl.append("sampfreq = {}".format(self.params.sampfreq))
        ctl.append("nsample = {}".format(self.params.nsample))

        ## write out the ctl file
        ctlhandle = os.path.realpath(
                "{}.ctl.txt".format(os.path.join(self.workdir, self._name)))
        # if isinstance(rep, int):
        #     ctlhandle = os.path.realpath(
        #         "{}-r{}.ctl.txt".format(os.path.join(self.workdir, self._name), rep))
        # else:
        #     ctlhandle = os.path.realpath(
        #         "{}.ctl.txt".format(os.path.join(self.workdir, self._name)))
        with open(ctlhandle, 'w') as out:
            out.write("\n".join(ctl))

        return ctlhandle