def _parse_00(ofile):
    """
    return 00 outfile as a pandas DataFrame
    """
    with open(ofile) as infile:
        ## read in the results summary from the end of the outfile
        arr = np.array(
            [" "] + infile.read().split("Summary of MCMC results\n\n\n")[1:][0]\
            .strip().split())

        ## reshape array 
        rows = 12
        cols = (arr.shape[0] + 1) / rows
        arr = arr.reshape(rows, cols)
        
        ## make into labeled data frame
        df = pd.DataFrame(
            data=arr[1:, 1:], 
            columns=arr[0, 1:], 
            index=arr[1:, 0],
            ).T
        return df