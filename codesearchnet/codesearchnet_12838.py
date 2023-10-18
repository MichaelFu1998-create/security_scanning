def run_bucky(self, ipyclient, force=False, quiet=False, subname=False):
        """
        Runs bucky for a given set of parameters and stores the result 
        to the ipa.bucky object. The results will be stored by default
        with the name '{name}-{alpha}' unless a argument is passed for
        'subname' to customize the output name. 

        Parameters:
        -----------
        subname (str):
            A custom name prefix for the output files produced by the bucky
            analysis and output into the {workdir}/{name} directory.
        force (bool):
            If True then existing result files with the same name prefix
            will be overwritten. 
        quiet (bool):
            If True the progress bars will be suppressed. 
        ipyclient (ipyparallel.Client)
            An active ipyparallel client to distribute jobs to.

        """

        ## check for existing results files
        minidir = os.path.realpath(os.path.join(self.workdir, self.name))
        infiles = glob.glob(os.path.join(minidir, "*.sumt"))
        outroot = os.path.realpath(os.path.join(self.workdir, self.name))

        ## build alpha list
        if isinstance(self.params.bucky_alpha, list):
            alphas = self.params.bucky_alpha
        else:
            alphas = [self.params.bucky_alpha]

        ## load balancer
        lbview = ipyclient.load_balanced_view()

        ## submit each to be processed
        asyncs = []
        for alpha in alphas:
            pathname = os.path.join(outroot, "CF-a"+str(alpha))
            if (os.path.exists(pathname)) and (force!=True):
                print("BUCKy results already exist for this object at alpha={}\n".format(alpha) +\
                      "use force=True to overwrite existing results")
            else:
                args = [
                    alpha, 
                    self.params.bucky_nchains, 
                    self.params.bucky_nreps, 
                    self.params.bucky_niter, 
                    pathname,
                    infiles]
                async = lbview.apply(_call_bucky, *args)
                asyncs.append(async)

        ## track progress
        start = time.time()
        printstr = "[bucky] infer CF posteriors     | {} | "
        while 1:
            ready = [i.ready() for i in asyncs]
            elapsed = datetime.timedelta(seconds=int(time.time()-start))
            if not quiet:            
                progressbar(len(ready), sum(ready), printstr.format(elapsed), spacer="")
            if len(ready) == sum(ready):
                if not quiet:
                    print("")
                break
            else:
                time.sleep(0.1)

        ## check success
        for async in asyncs:
            if not async.successful():
                raise IPyradWarningExit(async.result())