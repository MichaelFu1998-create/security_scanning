def write_usnps(data, sidx, pnames):
    """ write the bisnp string """

    ## grab bis data from tmparr
    tmparrs = os.path.join(data.dirs.outfiles, "tmp-{}.h5".format(data.name)) 
    with h5py.File(tmparrs, 'r') as io5:
        bisarr = io5["bisarr"]

        ## trim to size b/c it was made longer than actual
        end = np.where(np.all(bisarr[:] == "", axis=0))[0]
        if np.any(end):
            end = end.min()
        else:
            end = bisarr.shape[1]        

        ## write to usnps file
        with open(data.outfiles.usnpsphy, 'w') as out:
            out.write("{} {}\n".format(bisarr.shape[0], end))
            for idx, name in enumerate(pnames):
                out.write("{}{}\n".format(name, "".join(bisarr[idx, :end])))