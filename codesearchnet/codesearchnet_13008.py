def write_geno(data, sidx):
    """
    write the geno output formerly used by admixture, still supported by 
    adegenet, perhaps. Also, sNMF still likes .geno.
    """

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

        ## get most common base at each SNP as a pseudo-reference
        ## and record 0,1,2 or missing=9 for counts of the ref allele
        snpref = reftrick(snparr[:, :send].view(np.int8), GETCONS).view("S1")
        bisref = reftrick(bisarr[:, :bend].view(np.int8), GETCONS).view("S1")

        ## geno matrix to fill (9 is empty)
        snpgeno = np.zeros((snparr.shape[0], send), dtype=np.uint8)
        snpgeno.fill(9)
        bisgeno = np.zeros((bisarr.shape[0], bend), dtype=np.uint8)
        bisgeno.fill(9)

        ##--------------------------------------------------------------------
        ## fill in complete hits (match to first column ref base)
        mask2 = np.array(snparr[:, :send] == snpref[:, 0])
        snpgeno[mask2] = 2

        ## fill in single hits (heteros) match to hetero of first+second column
        ambref = np.apply_along_axis(lambda x: TRANSFULL[tuple(x)], 1, snpref[:, :2])
        mask1 = np.array(snparr[:, :send] == ambref)
        snpgeno[mask1] = 1

        ## fill in zero hits, meaning a perfect match to the second column base
        ## anything else is left at 9 (missing), b/c it's either missing or it
        ## is not bi-allelic. 
        mask0 = np.array(snparr[:, :send] == snpref[:, 1])
        snpgeno[mask0] = 0

        ##--------------------------------------------------------------------

        ## fill in complete hits
        mask2 = np.array(bisarr[:, :bend] == bisref[:, 0])
        bisgeno[mask2] = 2

        ## fill in single hits (heteros)
        ambref = np.apply_along_axis(lambda x: TRANSFULL[tuple(x)], 1, bisref[:, :2])
        mask1 = np.array(bisarr[:, :bend] == ambref)
        bisgeno[mask1] = 1

        ## fill in zero hits (match to second base)
        mask0 = np.array(bisarr[:, :bend] == bisref[:, 1])
        bisgeno[mask0] = 0

        ##---------------------------------------------------------------------
        ## print to files
        np.savetxt(data.outfiles.geno, snpgeno.T, delimiter="", fmt="%d")
        np.savetxt(data.outfiles.ugeno, bisgeno.T, delimiter="", fmt="%d")
    LOGGER.debug("finished writing geno in: %s", time.time() - start)