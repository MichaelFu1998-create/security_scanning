def _step5func(self, samples, force, ipyclient):
        """ hidden wrapped function to start step 5 """
        ## print header
        if self._headers:
            print("\n  Step 5: Consensus base calling ")

        ## Get sample objects from list of strings
        samples = _get_samples(self, samples)

        ## Check if all/none in the right state
        if not self._samples_precheck(samples, 5, force):
            raise IPyradError(FIRST_RUN_4)

        elif not force:
            ## skip if all are finished
            if all([i.stats.state >= 5 for i in samples]):
                print(CONSENS_EXIST.format(len(samples)))
                return
        ## pass samples to rawedit
        assemble.consens_se.run(self, samples, force, ipyclient)