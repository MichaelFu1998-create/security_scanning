def build_input_file(data, samples, randomseed):
    """
    [This is run on an ipengine]
    Make a concatenated consens file with sampled alleles (no RSWYMK/rswymk).
    Orders reads by length and shuffles randomly within length classes
    """

    ## get all of the consens handles for samples that have consens reads
    ## this is better than using sample.files.consens for selecting files
    ## b/c if they were moved we only have to edit data.dirs.consens

    ## scratch the statement above, people shouldn't be moving files, 
    ## they should be using merge/branch, and so sample.files.consens
    ## is needed to keep track of samples from different dirs if they
    ## are later merged into the same assembly.
    #conshandles = [os.path.join(data.dirs.consens, sample.name+".consens.gz") \
    #              for sample in samples if \
    #              sample.stats.reads_consens]
    conshandles = [sample.files.consens[0] \
                  for sample in samples if \
                  sample.stats.reads_consens]
    conshandles.sort()
    assert conshandles, "no consensus files found"

    ## concatenate all of the gzipped consens files
    cmd = ['cat'] + conshandles
    #allcons = os.path.join(data.dirs.consens, data.name+"_catcons.tmp")
    allcons = os.path.join(data.dirs.across, data.name+"_catcons.tmp")
    LOGGER.debug(" ".join(cmd))
    with open(allcons, 'w') as output:
        call = sps.Popen(cmd, stdout=output, close_fds=True)
        call.communicate()

    ## a string of sed substitutions for temporarily replacing hetero sites
    ## skips lines with '>', so it doesn't affect taxon names
    subs = ["/>/!s/W/A/g", "/>/!s/w/A/g", "/>/!s/R/A/g", "/>/!s/r/A/g",
            "/>/!s/M/A/g", "/>/!s/m/A/g", "/>/!s/K/T/g", "/>/!s/k/T/g",
            "/>/!s/S/C/g", "/>/!s/s/C/g", "/>/!s/Y/C/g", "/>/!s/y/C/g"]
    subs = ";".join(subs)

    ## impute pseudo-haplo information to avoid mismatch at hetero sites
    ## the read data with hetero sites is put back into clustered data later.
    ## pipe passed data from gunzip to sed.
    cmd1 = ["gunzip", "-c", allcons]
    cmd2 = ["sed", subs]
    LOGGER.debug(" ".join(cmd1))
    proc1 = sps.Popen(cmd1, stdout=sps.PIPE, close_fds=True)
    allhaps = allcons.replace("_catcons.tmp", "_cathaps.tmp")
    with open(allhaps, 'w') as output:
        LOGGER.debug(" ".join(cmd2))
        proc2 = sps.Popen(cmd2, stdin=proc1.stdout, stdout=output, close_fds=True)
        proc2.communicate()
    proc1.stdout.close()

    ## now sort the file using vsearch
    allsort = allcons.replace("_catcons.tmp", "_catsort.tmp")
    cmd1 = [ipyrad.bins.vsearch,
            "--sortbylength", allhaps,
            "--fasta_width", "0",
            "--output", allsort]
    LOGGER.debug(" ".join(cmd1))
    proc1 = sps.Popen(cmd1, close_fds=True)
    proc1.communicate()

    ## shuffle sequences within size classes. Tested seed (8/31/2016)
    ## shuffling works repeatably with seed.
    random.seed(randomseed)

    ## open an iterator to lengthsorted file and grab two lines at at time
    allshuf = allcons.replace("_catcons.tmp", "_catshuf.tmp")
    outdat = open(allshuf, 'w')
    indat = open(allsort, 'r')
    idat = itertools.izip(iter(indat), iter(indat))
    done = 0

    chunk = [idat.next()]
    while not done:
        ## grab 2-lines until they become shorter (unless there's only one)
        oldlen = len(chunk[-1][-1])
        while 1:
            try:
                dat = idat.next()
            except StopIteration:
                done = 1
                break
            if len(dat[-1]) == oldlen:
                chunk.append(dat)
            else:
                ## send the last chunk off to be processed
                random.shuffle(chunk)
                outdat.write("".join(itertools.chain(*chunk)))
                ## start new chunk
                chunk = [dat]
                break

    ## do the last chunk
    random.shuffle(chunk)
    outdat.write("".join(itertools.chain(*chunk)))

    indat.close()
    outdat.close()