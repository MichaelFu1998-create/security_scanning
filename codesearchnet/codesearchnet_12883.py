def run3(data, ipyclient, force):
    """
    One input file (or pair) is run on two processors, one for reading 
    and decompressing the data, and the other for demuxing it.
    """

    start = time.time()
    ## get file handles, name-lens, cutters, and matchdict, 
    ## and remove any existing files if a previous run failed.
    raws, longbar, cutters, matchdict = prechecks2(data, force)

    ## wrap funcs to ensure we can kill tmpfiles
    kbd = 0
    try:
        ## send chunks to be demux'd, nothing is parallelized yet.
        lbview = ipyclient.load_balanced_view()
        args = (data, raws, cutters, longbar, matchdict)
        async = lbview.apply(demux3, *args)

        ## track progress
        while 1:
            ## how many of this func have finished so far
            elapsed = datetime.timedelta(seconds=int(time.time()-start))
            printstr = ' writing/compressing   | {} | s1 |'
            progressbar(len(ready), sum(ready), printstr, spacer=spacer)
            time.sleep(0.1)
            if async.ready():
                print("")
                break
        
        if async.successful():
            statdicts = async.get()
        else:
            raise IPyradWarningExit(async.get())

        ## build stats from dictionaries
        perfile, fsamplehits, fbarhits, fmisses, fdbars = statdicts
        make_stats(data, perfile, fsamplehits, fbarhits, fmisses, fdbars)


    except KeyboardInterrupt:
        print("\n  ...interrupted, just a second while we ensure proper cleanup")
        kbd = 1

    ## cleanup
    finally:
        ## cleaning up the tmpdir is safe from ipyclient
        tmpdir = os.path.join(data.paramsdict["project_dir"], "tmp-chunks-"+data.name)
        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)

        tmpfiles = glob.glob(os.path.join(data.dirs.fastqs, "tmp_*_R*.fastq"))
        tmpfiles += glob.glob(os.path.join(data.dirs.fastqs, "tmp_*.p"))
        for tmpf in tmpfiles:
            if os.path.exists(tmpf):
                os.remove(tmpf)

        if kbd:
            raise