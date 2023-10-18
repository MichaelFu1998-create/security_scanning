def splitalleles(consensus):
    """ takes diploid consensus alleles with phase data stored as a mixture
    of upper and lower case characters and splits it into 2 alleles """

    ## store two alleles, allele1 will start with bigbase
    allele1 = list(consensus)
    allele2 = list(consensus)
    hidx = [i for (i, j) in enumerate(consensus) if j in "RKSWYMrkswym"]

    ## do remaining h sites
    for idx in hidx:
        hsite = consensus[idx]
        if hsite.isupper():
            allele1[idx] = PRIORITY[hsite]
            allele2[idx] = MINOR[hsite]
        else:
            allele1[idx] = MINOR[hsite.upper()]
            allele2[idx] = PRIORITY[hsite.upper()]

    ## convert back to strings
    allele1 = "".join(allele1)
    allele2 = "".join(allele2)

    return allele1, allele2