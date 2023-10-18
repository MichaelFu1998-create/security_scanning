def write_phy(data, sidx, pnames):
    """ 
    write the phylip output file from the tmparr[seqarray] 
    """

    ## grab seq data from tmparr
    start = time.time()
    tmparrs = os.path.join(data.dirs.outfiles, "tmp-{}.h5".format(data.name)) 
    with h5py.File(tmparrs, 'r') as io5:
        seqarr = io5["seqarr"]

        ## trim to size b/c it was made longer than actual
        end = np.where(np.all(seqarr[:] == "", axis=0))[0]
        if np.any(end):
            end = end.min()
        else:
            end = seqarr.shape[1] 

        ## write to phylip 
        with open(data.outfiles.phy, 'w') as out:
            ## write header
            out.write("{} {}\n".format(seqarr.shape[0], end))

            ## write data rows
            for idx, name in enumerate(pnames):
                out.write("{}{}\n".format(name, "".join(seqarr[idx, :end])))
    LOGGER.debug("finished writing phy in: %s", time.time() - start)