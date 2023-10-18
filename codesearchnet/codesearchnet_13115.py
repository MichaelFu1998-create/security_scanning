def run(self,
        kpop, 
        nreps, 
        ipyclient=None,
        seed=12345, 
        force=False,
        quiet=False, 
        ):

        """ 
        submits a job to run on the cluster and returns an asynchronous result
        object. K is the number of populations, randomseed if not set will be 
        randomly drawn, ipyclient if not entered will raise an error. If nreps
        is set then multiple jobs will be started from new seeds, each labeled
        by its replicate number. If force=True then replicates will be overwritten, 
        otherwise, new replicates will be created starting with the last file N 
        found in the workdir. 

        Parameters:
        -----------
        kpop: (int)
            The MAXPOPS parameter in structure, i.e., the number of populations
            assumed by the model (K). 

        nreps: (int):
            Number of independent runs starting from distinct seeds.

        ipyclient: (ipyparallel.Client Object)
            An ipyparallel client connected to an ipcluster instance. This is 
            used to manage parallel jobs. If not present a single job will
            run and block until finished (i.e., code is not parallel).

        seed: (int):
            Random number seed used for subsampling unlinked SNPs if a mapfile
            is linked to the Structure Object. 

        force: (bool):
            If force is true then old replicates are removed and new reps start
            from rep-0. Otherwise, new reps start at end of existing rep numbers.

        quiet: (bool)
            Whether to print number of jobs submitted to stderr

        Example: 
        ---------
        import ipyparallel as ipp
        import ipyrad.analysis as ipa

        ## get parallel client
        ipyclient = ipp.Client()

        ## get structure object
        s = ipa.structure(
                name="test",
                data="mydata.str", 
                mapfile="mydata.snps.map",
                workdir="structure-results",
                )

        ## modify some basic params
        s.mainparams.numreps = 100000
        s.mainparams.burnin = 10000

        ## submit many jobs
        for kpop in [3, 4, 5]:
            s.run(
                kpop=kpop, 
                nreps=10, 
                ipyclient=ipyclient,
                )

        ## block until all jobs finish
        ipyclient.wait()

        """
        ## initiate starting seed
        np.random.seed(seed)

        ## check for stuructre here
        proc = subprocess.Popen(["which", "structure"],
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT).communicate()
        if not proc:
            raise Exception(\
                "structure is not installed: run `conda install structure -c ipyrad`")

        ## start load balancer
        if ipyclient:
            lbview = ipyclient.load_balanced_view()

        ## remove old jobs with this same name
        handle = OPJ(self.workdir, self.name+"-K-{}-*".format(kpop))
        oldjobs = glob.glob(handle)
        if force or (not oldjobs):
            for job in oldjobs:
                os.remove(job)
            repstart = 0
            repend = nreps
        else:
            repstart = max([int(i.split("-")[-1][:-2]) for i in oldjobs])
            repend = repstart + nreps

        ## check that there is a ipcluster instance running
        for rep in xrange(repstart, repend):

            ## sample random seed for this rep
            self.extraparams.seed = np.random.randint(0, 1e9, 1)[0]

            ## prepare files (randomly subsamples snps if mapfile)
            mname, ename, sname = self.write_structure_files(kpop, rep)
            args = [
                mname, ename, sname,
                self.name, 
                self.workdir,
                self.extraparams.seed, 
                self.ntaxa, 
                self.nsites,
                kpop, 
                rep]

            if ipyclient:
                ## call structure
                async = lbview.apply(_call_structure, *(args))
                self.asyncs.append(async)

            else:
                if not quiet:
                    sys.stderr.write("submitted 1 structure job [{}-K-{}]\n"\
                                 .format(self.name, kpop))
                comm = _call_structure(*args)
                return comm

        if ipyclient:
            if not quiet:
                sys.stderr.write("submitted {} structure jobs [{}-K-{}]\n"\
                                .format(nreps, self.name, kpop))