def derep_and_sort(data, infile, outfile, nthreads):
    """
    Dereplicates reads and sorts so reads that were highly replicated are at
    the top, and singletons at bottom, writes output to derep file. Paired
    reads are dereplicated as one concatenated read and later split again.
    Updated this function to take infile and outfile to support the double
    dereplication that we need for 3rad (5/29/15 iao).
    """

    ## datatypes options
    strand = "plus"
    if "gbs" in data.paramsdict["datatype"]\
        or "2brad" in data.paramsdict["datatype"]:
        strand = "both"

    ## pipe in a gzipped file
    if infile.endswith(".gz"):
        catcmd = ["gunzip", "-c", infile]
    else:
        catcmd = ["cat", infile]

    ## do dereplication with vsearch
    cmd = [ipyrad.bins.vsearch,
            "--derep_fulllength", "-",
            "--strand", strand,
            "--output", outfile,
            "--threads", str(nthreads),
            "--fasta_width", str(0),
            "--fastq_qmax", "1000",
            "--sizeout", 
            "--relabel_md5",
            ]
    LOGGER.info("derep cmd %s", " ".join(cmd))

    ## run vsearch
    proc1 = sps.Popen(catcmd, stderr=sps.STDOUT, stdout=sps.PIPE, close_fds=True)
    proc2 = sps.Popen(cmd, stdin=proc1.stdout, stderr=sps.STDOUT, stdout=sps.PIPE, close_fds=True)

    try:
        errmsg = proc2.communicate()[0]
    except KeyboardInterrupt:
        LOGGER.info("interrupted during dereplication")
        raise KeyboardInterrupt()

    if proc2.returncode:
        LOGGER.error("error inside derep_and_sort %s", errmsg)
        raise IPyradWarningExit(errmsg)