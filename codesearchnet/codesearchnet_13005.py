def write_snps_map(data):
    """ write a map file with linkage information for SNPs file"""

    ## grab map data from tmparr
    start = time.time()
    tmparrs = os.path.join(data.dirs.outfiles, "tmp-{}.h5".format(data.name)) 
    with h5py.File(tmparrs, 'r') as io5:
        maparr = io5["maparr"][:]

        ## get last data 
        end = np.where(np.all(maparr[:] == 0, axis=1))[0]
        if np.any(end):
            end = end.min()
        else:
            end = maparr.shape[0]

        ## write to map file (this is too slow...)
        outchunk = []
        with open(data.outfiles.snpsmap, 'w') as out:
            for idx in xrange(end):
                ## build to list
                line = maparr[idx, :]
                #print(line)
                outchunk.append(\
                    "{}\trad{}_snp{}\t{}\t{}\n"\
                    .format(line[0], line[1], line[2], 0, line[3]))
                ## clear list
                if not idx % 10000:
                    out.write("".join(outchunk))
                    outchunk = []
            ## write remaining
            out.write("".join(outchunk))
    LOGGER.debug("finished writing snps_map in: %s", time.time() - start)