def singlecat(data, sample, bseeds, sidx, nloci):
    """
    Orders catg data for each sample into the final locus order. This allows
    all of the individual catgs to simply be combined later. They are also in
    the same order as the indels array, so indels are inserted from the indel
    array that is passed in.
    """

    LOGGER.info("in single cat here")
    ## enter ref data?
    isref = 'reference' in data.paramsdict["assembly_method"]

    ## grab seeds and hits info for this sample
    with h5py.File(bseeds, 'r') as io5:
        ## get hits just for this sample and sort them by sample order index
        hits = io5["uarr"][:]
        hits = hits[hits[:, 1] == sidx, :]
        #hits = hits[hits[:, 2].argsort()]
        ## get seeds just for this sample and sort them by sample order index
        seeds = io5["seedsarr"][:]
        seeds = seeds[seeds[:, 1] == sidx, :]
        #seeds = seeds[seeds[:, 2].argsort()]
        full = np.concatenate((seeds, hits))
        full = full[full[:, 0].argsort()]

    ## still using max+20 len limit, rare longer merged reads get trimmed
    ## we need to allow room for indels to be added too
    maxlen = data._hackersonly["max_fragment_length"] + 20

    ## we'll fill a new catg and alleles arr for this sample in locus order,
    ## which is known from seeds and hits
    ocatg = np.zeros((nloci, maxlen, 4), dtype=np.uint32)
    onall = np.zeros(nloci, dtype=np.uint8)
    ochrom = np.zeros((nloci, 3), dtype=np.int64)
    
    ## grab the sample's data and write to ocatg and onall
    if not sample.files.database:
        raise IPyradWarningExit("missing catg file - {}".format(sample.name))

    with h5py.File(sample.files.database, 'r') as io5:
        ## get it and delete it
        catarr = io5["catg"][:]
        tmp = catarr[full[:, 2], :maxlen, :]
        del catarr
        ocatg[full[:, 0], :tmp.shape[1], :] = tmp
        del tmp

        ## get it and delete it
        nall = io5["nalleles"][:]
        onall[full[:, 0]] = nall[full[:, 2]]
        del nall

        ## fill the reference data
        if isref:
            chrom = io5["chroms"][:]
            ochrom[full[:, 0]] = chrom[full[:, 2]]
            del chrom

    ## get indel locations for this sample
    ipath = os.path.join(data.dirs.across, data.name+".tmp.indels.hdf5")
    with h5py.File(ipath, 'r') as ih5:
        indels = ih5["indels"][sidx, :, :maxlen]

    ## insert indels into ocatg
    newcatg = inserted_indels(indels, ocatg)
    del ocatg, indels
    
    ## save individual tmp h5 data
    smpio = os.path.join(data.dirs.across, sample.name+'.tmp.h5')
    with h5py.File(smpio, 'w') as oh5:
        oh5.create_dataset("icatg", data=newcatg, dtype=np.uint32)
        oh5.create_dataset("inall", data=onall, dtype=np.uint8)
        if isref:
            oh5.create_dataset("ichrom", data=ochrom, dtype=np.int64)