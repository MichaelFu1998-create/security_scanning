def run(self, ipyclient):
        """
        parallelize calls to worker function.
        """
        
        ## connect to parallel client
        lbview = ipyclient.load_balanced_view()
        
        ## iterate over tests
        asyncs = []
        for test in xrange(self.ntests): 
            
            ## submit jobs to run
            async = lbview.apply(worker, self)
            asyncs.append(async)
            
        ## wait for jobs to finish
        ipyclient.wait()

        ## check for errors
        for async in asyncs:
            if not async.successful():
                raise Exception("Error: {}".format(async.result()))

        ## return results as df
        results = [i.result() for i in asyncs]
        self.results_table = pd.DataFrame(results)