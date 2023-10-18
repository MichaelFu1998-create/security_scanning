def _submit_jobs(self, 
        force, 
        ipyclient, 
        name_fields, 
        name_separator, 
        dry_run):
        """
        Download the accessions into a the designated workdir. 
        If file already exists it will only be overwritten if 
        force=True. Temporary files are removed. 
        """

        ## get Run data with default fields (1,4,6,30)
        df = self.fetch_runinfo(range(31), quiet=True)
        sys.stdout.flush()

        ## if not ipyclient then use multiprocessing
        if ipyclient:
            lb = ipyclient.load_balanced_view()

        ## if Run has samples with same name (replicates) then 
        ## we need to include the accessions in the file names
        if name_fields:
            ## indexing requires -1 ints
            fields = [int(i)-1 for i in fields_checker(name_fields)]
            ## make accession names, no spaces allowed
            df['Accession'] = pd.Series(df[df.columns[fields[0]]], index=df.index)
            for field in fields[1:]:
                df.Accession += name_separator + df[df.columns[field]]
            df.Accession = [i.replace(" ", "_") for i in df.Accession]    
            ## check that names are unique
            if not df.Accession.shape[0] == df.Accession.unique().shape[0]:
                raise IPyradWarningExit("names are not unique:\n{}"\
                    .format(df.Accession))

        ## backup default naming scheme
        else:
            if len(set(df.SampleName)) != len(df.SampleName):
                accs = (i+"-"+j for i, j in zip(df.SampleName, df.Run))
                df.Accession = accs
            else:
                df.Accession = df.SampleName

        if dry_run:
            print("\rThe following files will be written to: {}".format(self.workdir))
            print("{}\n".format(df.Accession))
        else:
            ## iterate over and download
            asyncs = []
            for idx in df.index:

                ## get args for this run
                srr = df.Run[idx]
                outname = df.Accession[idx]
                paired = df.spots_with_mates.values.astype(int).nonzero()[0].any()
                fpath = os.path.join(self.workdir, outname+".fastq.gz")

                ## skip if exists and not force
                skip = False
                if force:
                    if os.path.exists(fpath):
                        os.remove(fpath)
                else:
                    if os.path.exists(fpath):                
                        skip = True
                        sys.stdout.flush()
                        print("[skip] file already exists: {}".format(fpath))

                ## single job progress bar
                tidx = df.Accession.shape[0]
                #if not ipyclient:
                    

                ## submit job to run
                if not skip:
                    args = (self, srr, outname, paired)
                    if ipyclient:
                        async = lb.apply_async(call_fastq_dump_on_SRRs, *args)
                        asyncs.append(async)
                    else:
                        print("Downloading file {}/{}: {}".format(idx+1, tidx, fpath))
                        call_fastq_dump_on_SRRs(*args)
                        sys.stdout.flush()

            ## progress bar while blocking parallel
            if ipyclient:
                tots = df.Accession.shape[0]
                printstr = " Downloading fastq files | {} | "
                start = time.time()
                while 1:
                    elapsed = datetime.timedelta(seconds=int(time.time()-start))
                    ready = sum([i.ready() for i in asyncs])
                    progressbar(tots, ready, printstr.format(elapsed), spacer="")
                    time.sleep(0.1)
                    if tots == ready:
                        print("")
                        break
                self._report(tots)

                ## check for fails
                for async in asyncs:
                    if not async.successful():
                        raise IPyradWarningExit(async.result())