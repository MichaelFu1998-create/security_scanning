def cluster(data, sample, nthreads, force):
    """
    Calls vsearch for clustering. cov varies by data type, values were chosen
    based on experience, but could be edited by users
    """

    ## get the dereplicated reads
    if "reference" in data.paramsdict["assembly_method"]:
        derephandle = os.path.join(data.dirs.edits, sample.name+"-refmap_derep.fastq")
        ## In the event all reads for all samples map successfully then clustering
        ## the unmapped reads makes no sense, so just bail out.
        if not os.stat(derephandle).st_size:
            ## In this case you do have to create empty, dummy vsearch output
            ## files so building_clusters will not fail.
            uhandle = os.path.join(data.dirs.clusts, sample.name+".utemp")
            usort = os.path.join(data.dirs.clusts, sample.name+".utemp.sort")
            hhandle = os.path.join(data.dirs.clusts, sample.name+".htemp")
            for f in [uhandle, usort, hhandle]:
                open(f, 'a').close()
            return
    else:
        derephandle = os.path.join(data.dirs.edits, sample.name+"_derep.fastq")

    ## create handles for the outfiles
    uhandle = os.path.join(data.dirs.clusts, sample.name+".utemp")
    temphandle = os.path.join(data.dirs.clusts, sample.name+".htemp")

    ## If derep file doesn't exist then bail out
    if not os.path.isfile(derephandle):
        LOGGER.warn("Bad derephandle - {}".format(derephandle))
        raise IPyradError("Input file for clustering doesn't exist - {}"\
                        .format(derephandle))

    ## testing one sample fail
    #if sample.name == "1C_0":
    #    x

    ## datatype specific optimization
    ## minsl: the percentage of the seed that must be matched
    ##    smaller values for RAD/ddRAD where we might want to combine, say 50bp
    ##    reads and 100bp reads in the same analysis.
    ## query_cov: the percentage of the query sequence that must match seed
    ##    smaller values are needed for gbs where only the tips might overlap
    ##    larger values for pairgbs where they should overlap near completely
    ##    small minsl and high query cov allows trimmed reads to match to untrim
    ##    seed for rad/ddrad/pairddrad.
    strand = "plus"
    cov = 0.75
    minsl = 0.5
    if data.paramsdict["datatype"] in ["gbs", "2brad"]:
        strand = "both"
        cov = 0.5
        minsl = 0.5
    elif data.paramsdict["datatype"] == 'pairgbs':
        strand = "both"
        cov = 0.75
        minsl = 0.75

    ## If this value is not null (which is the default) then override query cov
    if data._hackersonly["query_cov"]:
        cov = str(data._hackersonly["query_cov"])
        assert float(cov) <= 1, "query_cov must be <= 1.0"

    ## get call string
    cmd = [ipyrad.bins.vsearch,
           "-cluster_smallmem", derephandle,
           "-strand", strand,
           "-query_cov", str(cov),
           "-id", str(data.paramsdict["clust_threshold"]),
           "-minsl", str(minsl),
           "-userout", uhandle,
           "-userfields", "query+target+id+gaps+qstrand+qcov",
           "-maxaccepts", "1",
           "-maxrejects", "0",
           "-threads", str(nthreads),
           "-notmatched", temphandle,
           "-fasta_width", "0",
           "-fastq_qmax", "100",
           "-fulldp",
           "-usersort"]

    ## not sure what the benefit of this option is exactly, needs testing,
    ## might improve indel detection on left side, but we don't want to enforce
    ## aligning on left side if not necessarily, since quality trimmed reads
    ## might lose bases on left side in step2 and no longer align.
    #if data.paramsdict["datatype"] in ["rad", "ddrad", "pairddrad"]:
    #    cmd += ["-leftjust"]

    ## run vsearch
    LOGGER.debug("%s", cmd)
    proc = sps.Popen(cmd, stderr=sps.STDOUT, stdout=sps.PIPE, close_fds=True)

    ## This is long running so we wrap it to make sure we can kill it
    try:
        res = proc.communicate()[0]
    except KeyboardInterrupt:
        proc.kill()
        raise KeyboardInterrupt

    ## check for errors
    if proc.returncode:
        LOGGER.error("error %s: %s", cmd, res)
        raise IPyradWarningExit("cmd {}: {}".format(cmd, res))