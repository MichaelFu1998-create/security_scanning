def _step3func(self, samples, noreverse, maxindels, force, ipyclient):
        """ hidden wrapped function to start step 3 """
        ## print headers
        if self._headers:
            print("\n  Step 3: Clustering/Mapping reads")

        ## Require reference seq for reference-based methods
        if self.paramsdict['assembly_method'] != "denovo":
            if not self.paramsdict['reference_sequence']:
                raise IPyradError(REQUIRE_REFERENCE_PATH\
                            .format(self.paramsdict["assembly_method"]))
            else:
                ## index the reference sequence
                ## Allow force to reindex the reference sequence
                ## send to run on the cluster. 
                lbview = ipyclient.load_balanced_view()
                async = lbview.apply(index_reference_sequence, *(self, force))

                ## print a progress bar for the indexing
                start = time.time()
                while 1:
                    elapsed = datetime.timedelta(seconds=int(time.time()-start))
                    printstr = " {}    | {} | s3 |".format("indexing reference", elapsed)
                    finished = int(async.ready())
                    progressbar(1, finished, printstr, spacer=self._spacer)
                    if finished:
                        print("")
                        break
                    time.sleep(0.9)
                ## error check
                if not async.successful():
                    raise IPyradWarningExit(async.result())

        ## Get sample objects from list of strings
        samples = _get_samples(self, samples)

        ## Check if all/none in the right state
        if not self._samples_precheck(samples, 3, force):
            raise IPyradError(FIRST_RUN_2)

        elif not force:
            ## skip if all are finished
            if all([i.stats.state >= 3 for i in samples]):
                print(CLUSTERS_EXIST.format(len(samples)))
                return

        ## run the step function
        assemble.cluster_within.run(self, samples, noreverse, maxindels,
                                    force, ipyclient)