def fill_dups_arr(data):
    """
    fills the duplicates array from the multi_muscle_align tmp files
    """
    ## build the duplicates array
    duplefiles = glob.glob(os.path.join(data.tmpdir, "duples_*.tmp.npy"))
    duplefiles.sort(key=lambda x: int(x.rsplit("_", 1)[-1][:-8]))

    ## enter the duplicates filter into super h5 array
    io5 = h5py.File(data.clust_database, 'r+')
    dfilter = io5["duplicates"]

    ## enter all duple arrays into full duplicates array
    init = 0
    for dupf in duplefiles:
        end = int(dupf.rsplit("_", 1)[-1][:-8])
        inarr = np.load(dupf)
        dfilter[init:end] = inarr
        init += end-init
        #os.remove(dupf)
    #del inarr

    ## continued progress bar
    LOGGER.info("all duplicates: %s", dfilter[:].sum())
    io5.close()