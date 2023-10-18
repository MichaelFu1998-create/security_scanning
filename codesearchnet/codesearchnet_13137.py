def nexmake(mdict, nlocus, dirs, mcmc_burnin, mcmc_ngen, mcmc_sample_freq):
    """ 
    function that takes a dictionary mapping names to 
    sequences, and a locus number, and writes it as a NEXUS
    file with a mrbayes analysis block.
    """
    ## create matrix as a string
    max_name_len = max([len(i) for i in mdict])
    namestring = "{:<" + str(max_name_len+1) + "} {}\n"
    matrix = ""
    for i in mdict.items():
        matrix += namestring.format(i[0], i[1])
    
    ## write nexus block
    handle = os.path.join(dirs, "{}.nex".format(nlocus))
    with open(handle, 'w') as outnex:
        outnex.write(NEXBLOCK.format(**{
            "ntax": len(mdict), 
            "nchar": len(mdict.values()[0]), 
            "matrix": matrix,
            "ngen": mcmc_ngen, 
            "sfreq": mcmc_sample_freq, 
            "burnin": mcmc_burnin, 
            }))