def _link_fastqs(self, path=None, force=False, append=False, splitnames="_",
        fields=None, ipyclient=None):
        """
        Create Sample objects from demultiplexed fastq files in sorted_fastq_path,
        or append additional fastq files to existing Samples. This provides
        more flexible file input through the API than available in step1 of the
        command line interface. If passed ipyclient it will run in parallel.

        Note
        ----
        This function is called during step 1 if files are specified in
        'sorted_fastq_path'.

        Parameters
        ----------
        path : str
            Path to the fastq files to be linked to Sample objects. The default
            location is to select all files in the 'sorted_fastq_path'.
            Alternatively a different path can be entered here.

        append : bool
            The default action is to overwrite fastq files linked to Samples if
            they already have linked files. Use append=True to instead append
            additional fastq files to a Sample (file names should be formatted
            the same as usual, e.g., [name]_R1_[optional].fastq.gz).

        splitnames : str
            A string character used to file names. In combination with the
            fields argument can be used to subselect filename fields names.

        fields : list
            A list of indices for the fields to be included in names after
            filnames are split on the splitnames character. Useful for appending
            sequence names which must match existing names. If the largest index
            is greater than the number of split strings in the name the index
            if ignored. e.g., [2,3,4] ## excludes 0, 1 and >4

        force : bool
            Overwrites existing Sample data and statistics.

        Returns
        -------
        str
            Prints the number of new Sample objects created and the number of
            fastq files linked to Sample objects in the Assembly object.
        """

        ## cannot both force and append at once
        if force and append:
            raise IPyradError("Cannot use force and append at the same time.")

        if self.samples and not (force or append):
            raise IPyradError("Files already linked to `{}`.".format(self.name)\
                +" Use force=True to replace all files, or append=True to add"
                +" additional files to existing Samples.")

        ## make sure there is a workdir and workdir/fastqdir
        self.dirs.fastqs = os.path.join(self.paramsdict["project_dir"],
                                        self.name+"_fastqs")
        if not os.path.exists(self.paramsdict["project_dir"]):
            os.mkdir(self.paramsdict["project_dir"])

        ## get path to data files
        if not path:
            path = self.paramsdict["sorted_fastq_path"]

        ## but grab fastq/fq/gz, and then sort
        fastqs = glob.glob(path)
        ## Assert files are not .bz2 format
        if any([i for i in fastqs if i.endswith(".bz2")]):
            raise IPyradError(NO_SUPPORT_FOR_BZ2.format(path))
        fastqs = [i for i in fastqs if i.endswith(".gz") \
                                    or i.endswith(".fastq") \
                                    or i.endswith(".fq")]
        fastqs.sort()
        LOGGER.debug("Linking these fastq files:\n{}".format(fastqs))

        ## raise error if no files are found
        if not fastqs:
            raise IPyradError(NO_FILES_FOUND_PAIRS\
                        .format(self.paramsdict["sorted_fastq_path"]))

        ## link pairs into tuples
        if 'pair' in self.paramsdict["datatype"]:
            ## check that names fit the paired naming convention
            ## trying to support flexible types (_R2_, _2.fastq)
            r1_try1 = [i for i in fastqs if "_R1_" in i]
            r1_try2 = [i for i in fastqs if i.endswith("_1.fastq.gz")]
            r1_try3 = [i for i in fastqs if i.endswith("_R1.fastq.gz")]

            r2_try1 = [i for i in fastqs if "_R2_" in i]
            r2_try2 = [i for i in fastqs if i.endswith("_2.fastq.gz")]
            r2_try3 = [i for i in fastqs if i.endswith("_R2.fastq.gz")]

            r1s = [r1_try1, r1_try2, r1_try3]
            r2s = [r2_try1, r2_try2, r2_try3]

            ## check that something was found
            if not r1_try1 + r1_try2 + r1_try3:
                raise IPyradWarningExit(
                    "Paired filenames are improperly formatted. See Documentation")
            if not r2_try1 + r2_try2 + r2_try3:
                raise IPyradWarningExit(
                    "Paired filenames are improperly formatted. See Documentation")

            ## find the one with the right number of R1s
            for idx, tri in enumerate(r1s):
                if len(tri) == len(fastqs)/2:
                    break
            r1_files = r1s[idx]
            r2_files = r2s[idx]

            if len(r1_files) != len(r2_files):
                raise IPyradWarningExit(R1_R2_name_error\
                    .format(len(r1_files), len(r2_files)))

            fastqs = [(i, j) for i, j in zip(r1_files, r2_files)]

        ## data are not paired, create empty tuple pair
        else:
            ## print warning if _R2_ is in names when not paired
            idx = 0
            if any(["_R2_" in i for i in fastqs]):
                print(NAMES_LOOK_PAIRED_WARNING)
            fastqs = [(i, "") for i in fastqs]

        ## counters for the printed output
        linked = 0
        appended = 0

        ## clear samples if force
        if force:
            self.samples = {}

        ## track parallel jobs
        linkjobs = {}
        if ipyclient:
            lbview = ipyclient.load_balanced_view()

        ## iterate over input files
        for fastqtuple in list(fastqs):
            assert isinstance(fastqtuple, tuple), "fastqs not a tuple."
            ## local counters
            createdinc = 0
            linkedinc = 0
            appendinc = 0
            ## remove file extension from name
            if idx == 0:
                sname = _name_from_file(fastqtuple[0], splitnames, fields)
            elif idx == 1:
                sname = os.path.basename(fastqtuple[0].rsplit("_1.fastq.gz", 1)[0])
            elif idx == 2:
                sname = os.path.basename(fastqtuple[0].rsplit("_R1.fastq.gz", 1)[0])
            LOGGER.debug("New Sample name {}".format(sname))

            if sname not in self.samples:
                ## create new Sample
                LOGGER.debug("Creating new sample - ".format(sname))
                self.samples[sname] = Sample(sname)
                self.samples[sname].stats.state = 1
                self.samples[sname].barcode = None
                self.samples[sname].files.fastqs.append(fastqtuple)
                createdinc += 1
                linkedinc += 1
            else:
                ## if not forcing, shouldn't be here with existing Samples
                if append:
                    #if fastqtuple not in self.samples[sname].files.fastqs:
                    self.samples[sname].files.fastqs.append(fastqtuple)
                    appendinc += 1

                elif force:
                    ## overwrite/create new Sample
                    LOGGER.debug("Overwriting sample - ".format(sname))
                    self.samples[sname] = Sample(sname)
                    self.samples[sname].stats.state = 1
                    self.samples[sname].barcode = None
                    self.samples[sname].files.fastqs.append(fastqtuple)
                    createdinc += 1
                    linkedinc += 1
                else:
                    print("""
        The files {} are already in Sample. Use append=True to append additional
        files to a Sample or force=True to replace all existing Samples.
        """.format(sname))

            ## support serial execution w/o ipyclient
            if not ipyclient:
                if any([linkedinc, createdinc, appendinc]):
                    gzipped = bool(fastqtuple[0].endswith(".gz"))
                    nreads = 0
                    for alltuples in self.samples[sname].files.fastqs:
                        nreads += _zbufcountlines(alltuples[0], gzipped)
                    self.samples[sname].stats.reads_raw = nreads/4
                    self.samples[sname].stats_dfs.s1["reads_raw"] = nreads/4
                    self.samples[sname].state = 1

                    LOGGER.debug("Got reads for sample - {} {}".format(sname,\
                                    self.samples[sname].stats.reads_raw))
                    #created += createdinc
                    linked += linkedinc
                    appended += appendinc

            ## do counting in parallel
            else:
                if any([linkedinc, createdinc, appendinc]):
                    gzipped = bool(fastqtuple[0].endswith(".gz"))
                    for sidx, tup in enumerate(self.samples[sname].files.fastqs):
                        key = sname+"_{}".format(sidx)
                        linkjobs[key] = lbview.apply(_bufcountlines,
                                                    *(tup[0], gzipped))
                    LOGGER.debug("sent count job for {}".format(sname))
                    #created += createdinc
                    linked += linkedinc
                    appended += appendinc

        ## wait for link jobs to finish if parallel
        if ipyclient:
            start = time.time()
            printstr = ' loading reads         | {} | s1 |'
            while 1:
                fin = [i.ready() for i in linkjobs.values()]
                elapsed = datetime.timedelta(seconds=int(time.time()-start))
                progressbar(len(fin), sum(fin),
                    printstr.format(elapsed), spacer=self._spacer)
                time.sleep(0.1)
                if len(fin) == sum(fin):
                    print("")
                    break

            ## collect link job results
            sampdict = {i:0 for i in self.samples}
            for result in linkjobs:
                sname = result.rsplit("_", 1)[0]
                nreads = linkjobs[result].result()
                sampdict[sname] += nreads

            for sname in sampdict:
                self.samples[sname].stats.reads_raw = sampdict[sname]/4
                self.samples[sname].stats_dfs.s1["reads_raw"] = sampdict[sname]/4
                self.samples[sname].state = 1

        ## print if data were linked
        #print("  {} new Samples created in '{}'.".format(created, self.name))
        if linked:
            ## double for paired data
            if 'pair' in self.paramsdict["datatype"]:
                linked = linked*2
            if self._headers:
                print("{}{} fastq files loaded to {} Samples.".\
                      format(self._spacer, linked, len(self.samples)))
            ## save the location where these files are located
            self.dirs.fastqs = os.path.realpath(os.path.dirname(path))

        if appended:
            if self._headers:
                print("{}{} fastq files appended to {} existing Samples.".\
                      format(self._spacer, appended, len(self.samples)))

        ## save step-1 stats. We don't want to write this to the fastq dir, b/c
        ## it is not necessarily inside our project dir. Instead, we'll write 
        ## this file into our project dir in the case of linked_fastqs.
        self.stats_dfs.s1 = self._build_stat("s1")
        self.stats_files.s1 = os.path.join(self.paramsdict["project_dir"],
                                           self.name+
                                           '_s1_demultiplex_stats.txt')
        with open(self.stats_files.s1, 'w') as outfile:
            self.stats_dfs.s1.fillna(value=0).astype(np.int).to_string(outfile)