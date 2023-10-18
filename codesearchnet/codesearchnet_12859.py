def _step2func(self, samples, force, ipyclient):
        """ hidden wrapped function to start step 2"""

        ## print header
        if self._headers:
            print("\n  Step 2: Filtering reads ")

        ## If no samples in this assembly then it means you skipped step1,
        if not self.samples.keys():
            raise IPyradWarningExit(FIRST_RUN_1)

        ## Get sample objects from list of strings, if API.
        samples = _get_samples(self, samples)

        if not force:
            ## print warning and skip if all are finished
            if all([i.stats.state >= 2 for i in samples]):
                print(EDITS_EXIST.format(len(samples)))
                return

        ## Run samples through rawedit
        assemble.rawedit.run2(self, samples, force, ipyclient)