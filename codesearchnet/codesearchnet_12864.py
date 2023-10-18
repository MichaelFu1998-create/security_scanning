def _step7func(self, samples, force, ipyclient):
        """ Step 7: Filter and write output files """

        ## Get sample objects from list of strings
        samples = _get_samples(self, samples)

        if self._headers:
            print("\n  Step 7: Filter and write output files for {} Samples".\
                  format(len(samples)))

        ## Check if all/none of the samples are in the self.database
        try:
            with h5py.File(self.clust_database, 'r') as io5:
                dbset = set(io5["seqs"].attrs['samples'])
                iset = set([i.name for i in samples])

                ## TODO: Handle the case where dbdiff is not empty?
                ## This might arise if someone tries to branch and remove
                ## samples at step 7.
                dbdiff = dbset.difference(iset)
                idiff = iset.difference(dbset)
                if idiff:
                    print(NOT_CLUSTERED_YET\
                    .format(self.database, ", ".join(list(idiff))))

                    ## The the old way that failed unless all samples were
                    ## clustered successfully in step 6. Adding some flexibility
                    ## to allow writing output even if some samples failed.
                    ## raise IPyradWarningExit(msg)

                    ## Remove the samples that aren't ready for writing out
                    ## i.e. only proceed with the samples that are actually
                    ## present in the db
                    samples = [x for x in samples if x.name not in idiff]
        except (IOError, ValueError):
            raise IPyradError(FIRST_RUN_6.format(self.clust_database))

        if not force:
            outdir = os.path.join(self.dirs.project, self.name+"_outfiles")
            if os.path.exists(outdir):
                raise IPyradWarningExit(OUTPUT_EXISTS.format(outdir))

        ## Run step7
        assemble.write_outfiles.run(self, samples, force, ipyclient)