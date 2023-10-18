def write_str(data, sidx, pnames):
    """ Write STRUCTURE format for all SNPs and unlinked SNPs """

    ## grab snp and bis data from tmparr
    start = time.time()
    tmparrs = os.path.join(data.dirs.outfiles, "tmp-{}.h5".format(data.name)) 
    with h5py.File(tmparrs, 'r') as io5:
        snparr = io5["snparr"]
        bisarr = io5["bisarr"]

        ## trim to size b/c it was made longer than actual
        bend = np.where(np.all(bisarr[:] == "", axis=0))[0]
        if np.any(bend):
            bend = bend.min()
        else:
            bend = bisarr.shape[1]        

        send = np.where(np.all(snparr[:] == "", axis=0))[0]       
        if np.any(send):
            send = send.min()
        else:
            send = snparr.shape[1]        

        ## write to str and ustr
        out1 = open(data.outfiles.str, 'w')
        out2 = open(data.outfiles.ustr, 'w')
        numdict = {'A': '0', 'T': '1', 'G': '2', 'C': '3', 'N': '-9', '-': '-9'}
        if data.paramsdict["max_alleles_consens"] > 1:
            for idx, name in enumerate(pnames):
                out1.write("{}\t\t\t\t\t{}\n"\
                    .format(name,
                    "\t".join([numdict[DUCT[i][0]] for i in snparr[idx, :send]])))
                out1.write("{}\t\t\t\t\t{}\n"\
                    .format(name,
                    "\t".join([numdict[DUCT[i][1]] for i in snparr[idx, :send]])))
                out2.write("{}\t\t\t\t\t{}\n"\
                    .format(name,
                    "\t".join([numdict[DUCT[i][0]] for i in bisarr[idx, :bend]])))
                out2.write("{}\t\t\t\t\t{}\n"\
                    .format(name,
                    "\t".join([numdict[DUCT[i][1]] for i in bisarr[idx, :bend]])))
        else:
            ## haploid output
            for idx, name in enumerate(pnames):
                out1.write("{}\t\t\t\t\t{}\n"\
                    .format(name,
                    "\t".join([numdict[DUCT[i][0]] for i in snparr[idx, :send]])))
                out2.write("{}\t\t\t\t\t{}\n"\
                    .format(name,
                    "\t".join([numdict[DUCT[i][0]] for i in bisarr[idx, :bend]])))
        out1.close()
        out2.close()
    LOGGER.debug("finished writing str in: %s", time.time() - start)