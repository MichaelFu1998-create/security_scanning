def run_mbsum(self, ipyclient, force=False, quiet=False):
        """
        Sums two replicate mrbayes runs for each locus
        """
        minidir = os.path.realpath(os.path.join(self.workdir, self.name))
        trees1 = glob.glob(os.path.join(minidir, "*.run1.t"))
        trees2 = glob.glob(os.path.join(minidir, "*.run2.t"))

        ## clear existing files 
        existing = glob.glob(os.path.join(self.workdir, self.name, "*.sumt"))
        if any(existing):
            if force:
                for rfile in existing:
                    os.remove(rfile)
            else:
                path = os.path.join(self.workdir, self.name)
                raise IPyradWarningExit(EXISTING_SUMT_FILES.format(path))

        ## load balancer
        lbview = ipyclient.load_balanced_view()

        ## submit each to be processed
        asyncs = []
        for tidx in xrange(len(trees1)):
            rep1 = trees1[tidx]
            rep2 = trees2[tidx]
            outname = os.path.join(minidir, str(tidx)+".sumt")
            async = lbview.apply(_call_mbsum, *(rep1, rep2, outname))
            asyncs.append(async)

        ## track progress
        start = time.time()
        printstr = "[mbsum] sum replicate runs      | {} | "
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