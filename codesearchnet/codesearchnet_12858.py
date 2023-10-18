def _step1func(self, force, ipyclient):
        """ hidden wrapped function to start step 1 """

        ## check input data files
        sfiles = self.paramsdict["sorted_fastq_path"]
        rfiles = self.paramsdict["raw_fastq_path"]

        ## do not allow both a sorted_fastq_path and a raw_fastq
        if sfiles and rfiles:
            raise IPyradWarningExit(NOT_TWO_PATHS)

        ## but also require that at least one exists
        if not (sfiles or rfiles):
            raise IPyradWarningExit(NO_SEQ_PATH_FOUND)

        ## print headers
        if self._headers:
            if sfiles:
                print("\n{}Step 1: Loading sorted fastq data to Samples"\
                      .format(self._spacer))
            else:
                print("\n{}Step 1: Demultiplexing fastq data to Samples"\
                    .format(self._spacer))

        ## if Samples already exist then no demultiplexing
        if self.samples:
            if not force:
                print(SAMPLES_EXIST.format(len(self.samples), self.name))
            else:
                ## overwrite existing data else do demux
                if glob.glob(sfiles):
                    self._link_fastqs(ipyclient=ipyclient, force=force)
                else:
                    assemble.demultiplex.run2(self, ipyclient, force)

        ## Creating new Samples
        else:
            ## first check if demultiplexed files exist in sorted path
            if glob.glob(sfiles):
                self._link_fastqs(ipyclient=ipyclient)

            ## otherwise do the demultiplexing
            else:
                assemble.demultiplex.run2(self, ipyclient, force)