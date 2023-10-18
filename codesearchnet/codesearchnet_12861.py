def _step4func(self, samples, force, ipyclient):
        """ hidden wrapped function to start step 4 """

        if self._headers:
            print("\n  Step 4: Joint estimation of error rate and heterozygosity")

        ## Get sample objects from list of strings
        samples = _get_samples(self, samples)

        ## Check if all/none in the right state
        if not self._samples_precheck(samples, 4, force):
            raise IPyradError(FIRST_RUN_3)

        elif not force:
            ## skip if all are finished
            if all([i.stats.state >= 4 for i in samples]):
                print(JOINTS_EXIST.format(len(samples)))
                return

        ## send to function
        assemble.jointestimate.run(self, samples, force, ipyclient)