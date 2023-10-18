def write_nex(data, sidx, pnames):
    """ 
    write the nexus output file from the tmparr[seqarray] and tmparr[maparr]
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

        ## write to nexus
        data.outfiles.nex = os.path.join(data.dirs.outfiles, data.name+".nex")

        with open(data.outfiles.nex, 'w') as out:

            ## write nexus seq header
            out.write(NEXHEADER.format(seqarr.shape[0], end))

            ## grab a big block of data
            chunksize = 100000  # this should be a multiple of 100
            for bidx in xrange(0, end, chunksize):
                bigblock = seqarr[:, bidx:bidx+chunksize]
                lend = end-bidx
                #LOGGER.info("BIG: %s %s %s %s", bigblock.shape, bidx, lend, end)

                ## write interleaved seqs 100 chars with longname+2 before
                tmpout = []            
                for block in xrange(0, min(chunksize, lend), 100):
                    stop = min(block+100, end)

                    for idx, name in enumerate(pnames):
                        seqdat = bigblock[idx, block:stop]
                        tmpout.append("  {}{}\n".format(name, "".join(seqdat)))
                    tmpout.append("\n")

                ## print intermediate result and clear
                if any(tmpout):
                    out.write("".join(tmpout))
            ## closer
            out.write(NEXCLOSER)
    LOGGER.debug("finished writing nex in: %s", time.time() - start)