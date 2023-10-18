def run(self,
        ipyclient, 
        nreps=1, 
        quiet=False,
        randomize_order=False,
        force=False,
        ):
        """
        Submits bpp jobs to run on a cluster (ipyparallel Client). 
        The seed for the random number generator if not set is randomly 
        drawn, and if multiple reps are submitted (nreps>1) then each will 
        draw a subsequent random seeds after that. An ipyclient connection 
        is required. Asynchronous result objects are stored in the bpp 
        object submitting the jobs. 
        
        Parameters:
        -----------
        nreps (int):
            submits nreps replicate jobs to the cluster each with a different 
            random seed drawn starting from the starting seed. 
        ipyclient (ipyparallel.Client)
            an ipyparallel.Client object connected to a running cluster. 
        quiet (bool):
            whether to print that the jobs have been submitted
        randomize_order (bool):
            if True then when maxloci is set this will randomly sample a 
            different set of N loci in each replicate, rather than sampling
            just the first N loci < maxloci. 
        force (bool):
            Overwrite existing files with the same name. Default=False, skip
            over existing files.
        """

        ## is this running algorithm 00?
        is_alg00 = (not self.params.infer_sptree) and (not self.params.infer_delimit)

        ## clear out pre-existing files for this object
        self.files.mcmcfiles = []
        self.files.outfiles = []
        self.files.treefiles = []
        self.asyncs = []

        ## initiate random seed
        np.random.seed(self.params.seed)

        ## load-balancer
        lbview = ipyclient.load_balanced_view()

        ## send jobs
        for job in xrange(nreps):

            ## make repname and make ctl filename
            self._name = "{}_r{}".format(self.name, job)
            ctlhandle = os.path.realpath(
                os.path.join(self.workdir, "{}.ctl.txt".format(self._name)))

            ## skip if ctlfile exists
            if (not force) and (os.path.exists(ctlhandle)):
                print("Named ctl file already exists. Use force=True to" \
                    +" overwrite\nFilename:{}".format(ctlhandle))
            else:
                ## change seed and ctl for each rep, this writes into the ctl
                ## file the correct name for the other files which share the 
                ## same rep number in their names.
                #self.params._seed = np.random.randint(0, 1e9, 1)[0]
                self._write_mapfile()
                #if randomize_order:
                self._write_seqfile(randomize_order=randomize_order)
                ctlfile = self._write_ctlfile()
                
                ## submit to engines
                async = lbview.apply(_call_bpp, *(self._kwargs["binary"], ctlfile, is_alg00))
                self.asyncs.append(async)

                ## save tree file if alg 00
                if is_alg00:
                    self.files.treefiles.append(
                        ctlfile.rsplit(".ctl.txt", 1)[0] + ".tre")

        if self.asyncs and (not quiet):
            sys.stderr.write("submitted {} bpp jobs [{}] ({} loci)\n"\
                             .format(nreps, self.name, self._nloci))