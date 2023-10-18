def _step6func(self, 
        samples, 
        noreverse, 
        force, 
        randomseed, 
        ipyclient, 
        **kwargs):
        """ 
        Hidden function to start Step 6. 
        """

        ## Get sample objects from list of strings
        samples = _get_samples(self, samples)

        ## remove samples that aren't ready
        csamples = self._samples_precheck(samples, 6, force)

        ## print CLI header
        if self._headers:
            print("\n  Step 6: Clustering at {} similarity across {} samples".\
                  format(self.paramsdict["clust_threshold"], len(csamples)))

        ## Check if all/none in the right state
        if not csamples:
            raise IPyradError(FIRST_RUN_5)

        elif not force:
            ## skip if all are finished
            if all([i.stats.state >= 6 for i in csamples]):
                print(DATABASE_EXISTS.format(len(samples)))
                return

        ## run if this point is reached. We no longer check for existing
        ## h5 file, since checking Sample states should suffice.
        assemble.cluster_across.run(
            self, 
            csamples, 
            noreverse,
            force, 
            randomseed, 
            ipyclient, 
            **kwargs)