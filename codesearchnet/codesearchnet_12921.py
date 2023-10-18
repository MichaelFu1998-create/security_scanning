def build_tmp_h5(data, samples):
    """ build tmp h5 arrays that can return quick access for nloci"""
    ## get samples and names, sorted
    snames = [i.name for i in samples]
    snames.sort()

    ## Build an array for quickly indexing consens reads from catg files.
    ## save as a npy int binary file.
    uhandle = os.path.join(data.dirs.across, data.name+".utemp.sort")
    bseeds = os.path.join(data.dirs.across, data.name+".tmparrs.h5")

    ## send as first async1 job
    get_seeds_and_hits(uhandle, bseeds, snames)