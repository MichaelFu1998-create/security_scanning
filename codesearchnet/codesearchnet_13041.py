def run(data, samples, noreverse, maxindels, force, ipyclient):
    """ run the major functions for clustering within samples """

    ## list of samples to submit to queue
    subsamples = []

    ## if sample is already done skip
    for sample in samples:
        ## If sample not in state 2 don't try to cluster it.
        if sample.stats.state < 2:
            print("""\
    Sample not ready for clustering. First run step2 on sample: {}""".\
    format(sample.name))
            continue

        if not force:
            if sample.stats.state >= 3:
                print("""\
    Skipping {}; aleady clustered. Use force to re-cluster""".\
    format(sample.name))
            else:
                if sample.stats.reads_passed_filter:
                    subsamples.append(sample)
        else:
            ## force to overwrite
            if sample.stats.reads_passed_filter:
                subsamples.append(sample)

    ## run subsamples
    if not subsamples:
        print("  No Samples ready to be clustered. First run step2().")

    else:
        ## arguments to apply_jobs, inst catches exceptions
        try:
            ## make dirs that are needed including tmpdir
            setup_dirs(data)

            ## if refmapping make filehandles that will be persistent
            if not data.paramsdict["assembly_method"] == "denovo":
                for sample in subsamples:
                    refmap_init(data, sample, force)

                    ## set thread-count to 2 for paired-data
                    nthreads = 2
            ## set thread-count to 1 for single-end data          
            else:
                nthreads = 1

            ## overwrite nthreads if value in _ipcluster dict
            if "threads" in data._ipcluster.keys():
                nthreads = int(data._ipcluster["threads"])

                ## if more CPUs than there are samples then increase threads
                _ncpus = len(ipyclient)
                if _ncpus > 2*len(data.samples):
                    nthreads *= 2

            ## submit jobs to be run on cluster
            args = [data, subsamples, ipyclient, nthreads, maxindels, force]
            new_apply_jobs(*args)


        finally:
            ## this can fail if jobs were not stopped properly and are still
            ## writing to tmpdir. don't cleanup if debug is on.
            try:
                log_level = logging.getLevelName(LOGGER.getEffectiveLevel())
                if not log_level == "DEBUG":

                    if os.path.exists(data.tmpdir):
                        shutil.rmtree(data.tmpdir)
                    ## get all refmap_derep.fastqs
                    rdereps = glob.glob(os.path.join(data.dirs.edits, "*-refmap_derep.fastq"))
                    ## Remove the unmapped fastq files
                    for rmfile in rdereps:
                        os.remove(rmfile)

            except Exception as _:
                LOGGER.warning("failed to cleanup files/dirs")