def splitfiles(data, raws, ipyclient):
    """ sends raws to be chunked"""

    ## create a tmpdir for chunked_files and a chunk optimizer 
    tmpdir = os.path.join(data.paramsdict["project_dir"], "tmp-chunks-"+data.name)
    if os.path.exists(tmpdir):
        shutil.rmtree(tmpdir)
    os.makedirs(tmpdir)

    ## chunk into 8M reads
    totalreads = estimate_optim(data, raws[0][0], ipyclient)
    optim = int(8e6)
    njobs = int(totalreads/(optim/4.)) * len(raws)

    ## if more files than cpus: no chunking
    nosplit = 0
    if (len(raws) > len(ipyclient)) or (totalreads < optim):
        nosplit = 1

    ## send slices N at a time. The dict chunkfiles stores a tuple of rawpairs
    ## dictionary to store asyncresults for sorting jobs
    start = time.time()
    chunkfiles = {}
    for fidx, tups in enumerate(raws):
        handle = os.path.splitext(os.path.basename(tups[0]))[0]
        ## if number of lines is > 20M then just submit it
        if nosplit:
            chunkfiles[handle] = [tups]
        else:
            ## chunk the file using zcat_make_temps
            chunklist = zcat_make_temps(data, tups, fidx, tmpdir, optim, njobs, start)
            chunkfiles[handle] = chunklist
    if not nosplit:
        print("")

    return chunkfiles