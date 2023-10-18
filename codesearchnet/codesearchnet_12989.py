def enter_pairs(iloc, pnames, snppad, edg, aseqs, asnps, smask, samplecov, locuscov, start):
    """ enters funcs for pairs """

    ## snps was created using only the selected samples.
    LOGGER.info("edges in enter_pairs %s", edg)
    seq1 = aseqs[iloc, :, edg[0]:edg[1]+1]
    snp1 = asnps[iloc, edg[0]:edg[1]+1, ]

    ## the 2nd read edges are +5 for the spacer
    seq2 = aseqs[iloc, :, edg[2]:edg[3]+1]
    snp2 = asnps[iloc, edg[2]:edg[3]+1, ]

    ## remove rows with all Ns, seq has only selected samples
    nalln = np.all(seq1 == "N", axis=1)

    ## make mask of removed rows and excluded samples. Use the inverse
    ## of this to save the coverage for samples
    nsidx = nalln + smask
    LOGGER.info("nsidx %s, nalln %s, smask %s", nsidx, nalln, smask)
    samplecov = samplecov + np.invert(nsidx).astype(np.int32)
    LOGGER.info("samplecov %s", samplecov)
    idx = np.sum(np.invert(nsidx).astype(np.int32))
    LOGGER.info("idx %s", idx)
    locuscov[idx] += 1

    ## select the remaining names in order
    seq1 = seq1[~nsidx, ]
    seq2 = seq2[~nsidx, ]
    names = pnames[~nsidx]

    ## save string for printing, excluding names not in samples
    outstr = "\n".join(\
        [name + s1.tostring()+"nnnn"+s2.tostring() for name, s1, s2 in \
         zip(names, seq1, seq2)])

    #LOGGER.info("s1 %s", s1.tostring())
    #LOGGER.info("s2 %s", s2.tostring())

    ## get snp string and add to store
    snpstring1 = ["-" if snp1[i, 0] else \
                 "*" if snp1[i, 1] else \
                 " " for i in range(len(snp1))]
    snpstring2 = ["-" if snp2[i, 0] else \
                 "*" if snp2[i, 1] else \
                 " " for i in range(len(snp2))]

    #npis = str(snpstring1+snpstring2).count("*")
    #nvars = str(snpstring1+snpstring2).count("-") + npis
    outstr += "\n" + snppad + "".join(snpstring1)+\
              "    "+"".join(snpstring2)+"|{}|".format(iloc+start)
              #"|LOCID={},DBID={},NVAR={},NPIS={}|"\
              #.format(1+iloc+start, iloc, nvars, npis)

    return outstr, samplecov, locuscov