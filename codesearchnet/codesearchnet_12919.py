def build_h5_array(data, samples, nloci):
    """
    Sets up all of the h5 arrays that we will fill. 
    The catg array of prefiltered loci  is 4-dimensional (Big), so one big 
    array would overload memory, we need to fill it in slices. 
    This will be done in multicat (singlecat) and fill_superseqs.
    """

    ## sort to ensure samples will be in alphabetical order, tho they should be.
    samples.sort(key=lambda x: x.name)

    ## get maxlen dim
    maxlen = data._hackersonly["max_fragment_length"] + 20
    LOGGER.info("maxlen inside build_h5_array is %s", maxlen)
    LOGGER.info("nloci inside build_h5_array is %s", nloci)

    ## open new h5 handle
    data.clust_database = os.path.join(data.dirs.across, data.name+".clust.hdf5")
    io5 = h5py.File(data.clust_database, 'w')

    ## chunk to approximately 2 chunks per core
    chunks = ((nloci // (data.cpus*2)) + (nloci % (data.cpus*2)))

    ## Number of elements in hdf5 chunk may not exceed 500MB
    ## This is probably not actually optimal, to have such
    ## enormous chunk sizes, could probably explore efficiency
    ## of smaller chunk sizes on very very large datasets
    chunklen = chunks * len(samples) * maxlen * 4
    while chunklen > int(500e6):
        chunks = (chunks // 2) + (chunks % 2)
        chunklen = chunks * len(samples) * maxlen * 4
    LOGGER.info("chunks in build_h5_array: %s", chunks)

    data.chunks = chunks
    LOGGER.info("nloci is %s", nloci)
    LOGGER.info("chunks is %s", data.chunks)

    ## INIT FULL CATG ARRAY
    ## store catgs with a .10 loci chunk size
    supercatg = io5.create_dataset("catgs", (nloci, len(samples), maxlen, 4),
                                    dtype=np.uint32,
                                    chunks=(chunks, 1, maxlen, 4),
                                    compression="gzip")
    superseqs = io5.create_dataset("seqs", (nloci, len(samples), maxlen),
                                    dtype="|S1",
                                    #dtype=np.uint8,
                                    chunks=(chunks, len(samples), maxlen),
                                    compression='gzip')
    superalls = io5.create_dataset("nalleles", (nloci, len(samples)),
                                    dtype=np.uint8,
                                    chunks=(chunks, len(samples)),
                                    compression="gzip")
    superchroms = io5.create_dataset("chroms", (nloci, 3), 
                                     dtype=np.int64, 
                                     chunks=(chunks, 3),
                                     compression="gzip")

    ## allele count storage
    supercatg.attrs["chunksize"] = (chunks, 1, maxlen, 4)
    supercatg.attrs["samples"] = [i.name for i in samples]
    superseqs.attrs["chunksize"] = (chunks, len(samples), maxlen)
    superseqs.attrs["samples"] = [i.name for i in samples]
    superalls.attrs["chunksize"] = (chunks, len(samples))
    superalls.attrs["samples"] = [i.name for i in samples]
    superchroms.attrs["chunksize"] = (chunks, len(samples))
    superchroms.attrs["samples"] = [i.name for i in samples]

    ## array for pair splits locations, dup and ind filters
    io5.create_dataset("splits", (nloci, ), dtype=np.uint16)
    io5.create_dataset("duplicates", (nloci, ), dtype=np.bool_)

    ## close the big boy
    io5.close()