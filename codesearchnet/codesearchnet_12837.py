def run_mrbayes(self, ipyclient, force=False, quiet=False):
        """
        calls the mrbayes block in each nexus file.
        """

        ## get all the nexus files for this object
        minidir = os.path.realpath(os.path.join(self.workdir, self.name))
        nexus_files = glob.glob(os.path.join(minidir, "*.nex"))

        ## clear existing files 
        #existing = glob.glob(os.path.join(self.workdir, self.name, "*.nex"))
        existing = glob.glob(os.path.join(minidir, "*.nex.*"))
        if any(existing):
            if force:
                for rfile in existing:
                    os.remove(rfile)
            else:
                raise IPyradWarningExit(EXISTING_NEXdot_FILES.format(minidir))

        ## write new nexus files, or should users do that before this?
        #self.write_nexus_files(force=True)

        ## load balancer
        lbview = ipyclient.load_balanced_view()

        ## submit each to be processed
        asyncs = []
        for nex in nexus_files:
            async = lbview.apply(_call_mb, nex)
            asyncs.append(async)

        ## track progress
        start = time.time()
        printstr = "[mb] infer gene-tree posteriors | {} | "        
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