def run(self, 
        force=False, 
        ipyclient=None, 
        name_fields=30, 
        name_separator="_", 
        dry_run=False):
        """
        Download the accessions into a the designated workdir. 

        Parameters
        ----------
        force: (bool)
            If force=True then existing files with the same name
            will be overwritten. 

        ipyclient: (ipyparallel.Client)
            If provided, work will be distributed across a parallel
            client, otherwise download will be run on a single core.

        name_fields: (int, str):
            Provide the index of the name fields to be used as a prefix
            for fastq output files. The default is 30, which is the 
            SampleName field. Use sra.fetch_fields to see all available
            fields and their indices. A likely alternative is 1 (Run). 
            If multiple are listed then they will be joined by a "_" 
            character. For example (29,30) would yield something like:
            latin-name_sample-name (e.g., mus_musculus-NR10123).

        dry_run: (bool)
            If True then a table of file names that _would_ be downloaded
            will be shown, but the actual files will note be downloaded.
        """

        ## temporarily set directory for tmpfiles used by fastq-dump
        ## if this fails then just skip it.
        try:
            ## ensure output directory, also used as tmpdir
            if not os.path.exists(self.workdir):
                os.makedirs(self.workdir)

            ## get original directory for sra files 
            ## probably /home/ncbi/public/sra by default.
            self._set_vdbconfig_path()

            ## register ipyclient for cleanup
            if ipyclient:
                self._ipcluster["pids"] = {}
                for eid in ipyclient.ids:
                    engine = ipyclient[eid]
                    if not engine.outstanding:
                        pid = engine.apply(os.getpid).get()
                        self._ipcluster["pids"][eid] = pid               

            ## submit jobs to engines or local 
            self._submit_jobs(
                force=force, 
                ipyclient=ipyclient, 
                name_fields=name_fields, 
                name_separator=name_separator,
                dry_run=dry_run,
                )

        except IPyradWarningExit as inst:
            print(inst)
        ## exceptions to catch, cleanup and handle ipyclient interrupts
        except KeyboardInterrupt:
            print("keyboard interrupt...")
        except Exception as inst:
            print("Exception in run() - {}".format(inst))
        finally:
            ## reset working sra path
            self._restore_vdbconfig_path()

            ## if it made a new sra directory then it should be empty when 
            ## we are finished if all .sra files were removed. If so, then
            ## let's also remove the dir. if not empty, leave it.
            sradir = os.path.join(self.workdir, "sra")
            if os.path.exists(sradir) and (not os.listdir(sradir)):
                shutil.rmtree(sradir)
            else:
                ## print warning
                try:
                    print(FAILED_DOWNLOAD.format(os.listdir(sradir)))
                except OSError as inst:
                    ## If sra dir doesn't even exist something very bad is broken.
                    raise IPyradWarningExit("Download failed. Exiting.")
                ## remove fastq file matching to cached sra file
                for srr in os.listdir(sradir):
                    isrr = srr.split(".")[0]
                    ipath = os.path.join(self.workdir, "*_{}*.gz".format(isrr))
                    ifile = glob.glob(ipath)[0]
                    if os.path.exists(ifile):
                        os.remove(ifile)
                ## remove cache of sra files
                shutil.rmtree(sradir)

            ## cleanup ipcluster shutdown
            if ipyclient:
                ## send SIGINT (2) to all engines still running tasks
                try:
                    ipyclient.abort()
                    time.sleep(0.5)
                    for engine_id, pid in self._ipcluster["pids"].items():
                        if ipyclient.queue_status()[engine_id]["tasks"]:
                            os.kill(pid, 2)
                        time.sleep(0.1)
                except ipp.NoEnginesRegistered:
                    pass
                ## clean memory space
                if not ipyclient.outstanding:
                    ipyclient.purge_everything()
                ## uh oh, kill everything, something bad happened
                else:
                    ipyclient.shutdown(hub=True, block=False)
                    ipyclient.close()
                    print("\nwarning: ipcluster shutdown and must be restarted")