def sub_build_indels(data, samples):
    """ sub func in `build_indels()`. """

    ## get file handles
    indelfiles = glob.glob(os.path.join(data.tmpdir, "indels_*.tmp.npy"))
    alignbits = glob.glob(os.path.join(data.tmpdir, "align_*.fa"))

    ## sort into input order by chunk names
    indelfiles.sort(key=lambda x: int(x.rsplit("_", 1)[-1][:-8]))
    alignbits.sort(key=lambda x: int(x.rsplit("_", 1)[-1][:-3]))
    LOGGER.info("indelfiles %s", indelfiles)
    LOGGER.info("alignbits %s", alignbits)
    chunksize = int(indelfiles[0].rsplit("_", 1)[-1][:-8])

    ## concatenate finished seq clusters into a tmp file
    outhandle = os.path.join(data.dirs.across, data.name+"_catclust.gz")
    concatclusts(outhandle, alignbits)

    ## get dims for full indel array
    maxlen = data._hackersonly["max_fragment_length"] + 20
    nloci = get_nloci(data)
    LOGGER.info("maxlen inside build is %s", maxlen)
    LOGGER.info("nloci for indels %s", nloci)

    ## INIT TEMP INDEL ARRAY
    ## build an indel array for ALL loci in cat.clust.gz,
    ## chunked so that individual samples can be pulled out
    ipath = os.path.join(data.dirs.across, data.name+".tmp.indels.hdf5")
    with h5py.File(ipath, 'w') as io5:
        iset = io5.create_dataset(
            "indels",
            shape=(len(samples), nloci, maxlen),
            dtype=np.bool_,
            chunks=(1, chunksize, maxlen))

        ## again make sure names are ordered right
        samples.sort(key=lambda x: x.name)

        #iset.attrs["chunksize"] = (1, data.nloci, maxlen)
        iset.attrs["samples"] = [i.name for i in samples]

        ## enter all tmpindel arrays into full indel array
        done = 0
        init = 0
        for indf in indelfiles:
            end = int(indf.rsplit("_", 1)[-1][:-8])
            inarr = np.load(indf)
            LOGGER.info('inarr shape %s', inarr.shape)
            LOGGER.info('iset shape %s', iset.shape)
            iset[:, init:end, :] = inarr[:, :end-init]
            init += end-init
            done += 1
            print(done)