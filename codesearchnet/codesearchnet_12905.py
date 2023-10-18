def _parse_01(ofiles, individual=False):
    """ 
    a subfunction for summarizing results
    """

    ## parse results from outfiles
    cols = []
    dats = []
    for ofile in ofiles:

        ## parse file
        with open(ofile) as infile:
            dat  = infile.read()
        lastbits = dat.split(".mcmc.txt\n\n")[1:]
        results = lastbits[0].split("\n\n")[0].split()

        ## get shape from ...
        shape = (((len(results) - 3) / 4), 4)
        dat = np.array(results[3:]).reshape(shape)
        cols.append(dat[:, 3].astype(float))
        
    if not individual:
        ## get mean results across reps
        cols = np.array(cols)
        cols = cols.sum(axis=0) / len(ofiles) #10.
        dat[:, 3] = cols.astype(str)

        ## format as a DF
        df = pd.DataFrame(dat[:, 1:])
        df.columns = ["delim", "prior", "posterior"]
        nspecies = 1 + np.array([list(i) for i in dat[:, 1]], dtype=int).sum(axis=1)
        df["nspecies"] = nspecies
        return df
    
    else:
        ## get mean results across reps
        #return cols
        res = []
        for i in xrange(len(cols)):
            x = dat
            x[:, 3] = cols[i].astype(str)
            x = pd.DataFrame(x[:, 1:])
            x.columns = ['delim', 'prior', 'posterior']
            nspecies = 1 + np.array([list(i) for i in dat[:, 1]], dtype=int).sum(axis=1)
            x["nspecies"] = nspecies
            res.append(x)
        return res