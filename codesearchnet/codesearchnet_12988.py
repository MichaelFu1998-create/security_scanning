def locichunk(args):
    """
    Function from make_loci to apply to chunks. smask is sample mask.
    """
    ## parse args
    data, optim, pnames, snppad, smask, start, samplecov, locuscov, upper = args

    ## this slice
    hslice = [start, start+optim]

    ## get filter db info
    co5 = h5py.File(data.database, 'r')
    afilt = co5["filters"][hslice[0]:hslice[1], ]
    aedge = co5["edges"][hslice[0]:hslice[1], ]
    asnps = co5["snps"][hslice[0]:hslice[1], ]

    ## get seqs db
    io5 = h5py.File(data.clust_database, 'r')
    if upper:
        aseqs = np.char.upper(io5["seqs"][hslice[0]:hslice[1], ])
    else:
        aseqs = io5["seqs"][hslice[0]:hslice[1], ]

    ## which loci passed all filters
    keep = np.where(np.sum(afilt, axis=1) == 0)[0]
    store = []

    ## write loci that passed after trimming edges, then write snp string
    for iloc in keep:
        edg = aedge[iloc]
        #LOGGER.info("!!!!!! iloc edg %s, %s", iloc, edg)
        args = [iloc, pnames, snppad, edg, aseqs, asnps, smask, samplecov, locuscov, start]
        if edg[4]:
            outstr, samplecov, locuscov = enter_pairs(*args)
            store.append(outstr)
        else:
            outstr, samplecov, locuscov = enter_singles(*args)
            store.append(outstr)

    ## write to file and clear store
    tmpo = os.path.join(data.dirs.outfiles, data.name+".loci.{}".format(start))
    with open(tmpo, 'w') as tmpout:
        tmpout.write("\n".join(store) + "\n")

    ## close handles
    io5.close()
    co5.close()

    ## return sample counter
    return samplecov, locuscov, start