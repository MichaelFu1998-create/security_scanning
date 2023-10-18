def dstat(inarr, taxdict, mindict=1, nboots=1000, name=0):
    """ private function to perform a single D-stat test"""

    #if isinstance(inarr, str):
    #    with open(inarr, 'r') as infile:
    #        inarr = infile.read().strip().split("|\n")

    # ## get data as an array from loci file
    # ## if loci-list then parse arr from loci
    if isinstance(inarr, list):
        arr, _ = _loci_to_arr(inarr, taxdict, mindict)
    
    # ## if it's an array already then go ahead
    # elif isinstance(inarr, np.ndarray):
    #     arr = inarr
    # ## if it's a simulation object get freqs from array
    # elif isinstance(inarr, Sim):
    #     arr = _msp_to_arr(inarr, taxdict)

    #elif isinstance(inarr, types.GeneratorType):
    #    arr = _msp_to_arr(inarr, taxdict)
    #elif isinstance(inarr, list):
    #    arr = _msp_to_arr(inarr, taxdict)
    ## get data from Sim object, do not digest the ms generator
    #else:
    #    raise Exception("Must enter either a 'locifile' or 'arr'")

    ## run tests
    #if len(taxdict) == 4:
    if arr.shape[1] == 4:

        ## get results
        res, boots = _get_signif_4(arr, nboots)
    
        ## make res into a nice DataFrame
        res = pd.DataFrame(res, 
            columns=[name],
            index=["Dstat", "bootmean", "bootstd", "Z", "ABBA", "BABA", "nloci"])

    else:
        ## get results
        res, boots = _get_signif_5(arr, nboots)
         ## make int a DataFrame
        res = pd.DataFrame(res,
            index=["p3", "p4", "shared"], 
            columns=["Dstat", "bootmean", "bootstd", "Z", "ABxxA", "BAxxA", "nloci"]
            )

    return res.T, boots