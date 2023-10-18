def init_arrays(data):
    """
    Create database file for storing final filtered snps data as hdf5 array.
    Copies splits and duplicates info from clust_database to database.
    """

    ## get stats from step6 h5 and create new h5
    co5 = h5py.File(data.clust_database, 'r')
    io5 = h5py.File(data.database, 'w')

    ## get maxlen and chunk len
    maxlen = data._hackersonly["max_fragment_length"] + 20
    chunks = co5["seqs"].attrs["chunksize"][0]
    nloci = co5["seqs"].shape[0]

    ## make array for snp string, 2 cols, - and *
    snps = io5.create_dataset("snps", (nloci, maxlen, 2),
                              dtype=np.bool,
                              chunks=(chunks, maxlen, 2),
                              compression='gzip')
    snps.attrs["chunksize"] = chunks
    snps.attrs["names"] = ["-", "*"]

    ## array for filters that will be applied in step7
    filters = io5.create_dataset("filters", (nloci, 6), dtype=np.bool)
    filters.attrs["filters"] = ["duplicates", "max_indels",
                                "max_snps", "max_shared_hets",
                                "min_samps", "max_alleles"]

    ## array for edgetrimming
    edges = io5.create_dataset("edges", (nloci, 5),
                               dtype=np.uint16,
                               chunks=(chunks, 5),
                               compression="gzip")
    edges.attrs["chunksize"] = chunks
    edges.attrs["names"] = ["R1_L", "R1_R", "R2_L", "R2_R", "sep"]

    ## xfer data from clustdb to finaldb
    edges[:, 4] = co5["splits"][:]
    filters[:, 0] = co5["duplicates"][:]

    ## close h5s
    io5.close()
    co5.close()