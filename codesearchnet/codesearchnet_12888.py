def putstats(pfile, handle, statdicts):
    """ puts stats from pickles into a dictionary """

    ## load in stats
    with open(pfile, 'r') as infile:
        filestats, samplestats = pickle.load(infile)

    ## get dicts from statdicts tuple
    perfile, fsamplehits, fbarhits, fmisses, fdbars = statdicts

    ## pull new stats
    #handle = os.path.splitext(os.path.basename(handle))[0]
    perfile[handle] += filestats

    ## update sample stats
    samplehits, barhits, misses, dbars = samplestats
    fsamplehits.update(samplehits)
    fbarhits.update(barhits)
    fmisses.update(misses)
    fdbars.update(dbars)

    ## repack the tuple and return
    statdicts = perfile, fsamplehits, fbarhits, fmisses, fdbars
    return statdicts