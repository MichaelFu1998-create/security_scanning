def run2(data, ipyclient, force):
    """
    One input file (or pair) is run on two processors, one for reading 
    and decompressing the data, and the other for demuxing it.
    """

    ## get file handles, name-lens, cutters, and matchdict
    raws, longbar, cutters, matchdict = prechecks2(data, force)

    ## wrap funcs to ensure we can kill tmpfiles
    kbd = 0
    try:
        ## if splitting files, split files into smaller chunks for demuxing
        chunkfiles = splitfiles(data, raws, ipyclient)

        ## send chunks to be demux'd
        statdicts = demux2(data, chunkfiles, cutters, longbar, matchdict, ipyclient)

        ## concat tmp files
        concat_chunks(data, ipyclient)

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

        if kbd:
            raise KeyboardInterrupt("s1")
        else:
            _cleanup_and_die(data)