def enter_singles(iloc, pnames, snppad, edg, aseqs, asnps, smask, samplecov, locuscov, start):
    """ enter funcs for SE or merged data """

    ## grab all seqs between edges
    seq = aseqs[iloc, :, edg[0]:edg[1]+1]
    ## snps was created using only the selected samples, and is edge masked.
    ## The mask is for counting snps quickly, but trimming is still needed here
    ## to make the snps line up with the seqs in the snp string.
    snp = asnps[iloc, edg[0]:edg[1]+1, ]

    ## remove rows with all Ns, seq has only selected samples
    nalln = np.all(seq == "N", axis=1)

    ## make mask of removed rows and excluded samples. Use the inverse
    ## of this to save the coverage for samples
    nsidx = nalln + smask
    samplecov = samplecov + np.invert(nsidx).astype(np.int32)
    idx = np.sum(np.invert(nsidx).astype(np.int32))
    locuscov[idx] += 1

    ## select the remaining names in order
    seq = seq[~nsidx, ]
    names = pnames[~nsidx]

    ## save string for printing, excluding names not in samples
    outstr = "\n".join(\
        [name + s.tostring() for name, s in zip(names, seq)])

    ## get snp string and add to store
    snpstring = ["-" if snp[i, 0] else \
                 "*" if snp[i, 1] else \
                 " " for i in range(len(snp))]
    outstr += "\n" + snppad + "".join(snpstring) + "|{}|".format(iloc+start)
    #LOGGER.info("outstr %s", outstr)
    return outstr, samplecov, locuscov