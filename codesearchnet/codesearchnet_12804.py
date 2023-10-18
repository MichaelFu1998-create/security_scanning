def loci2cf(name, locifile, popdict, wdir=None, ipyclient=None):
    """ 
    Convert ipyrad .loci file to an iqtree-pomo 'counts' file

    Parameters:
    -----------
    name:
        A prefix name for output files that will be produced
    locifile:
        A .loci file produced by ipyrad.
    popdict: 
        A python dictionary grouping Clade names to Sample names. 
        Example: {"A": ['a', 'b', 'c'], "B": ['d', 'e', 'f']}
    ipyclient:
        If you pass it an ipyclient it will distribute work over
        remote engines, otherwise we use multiprocessing (todo).
    """

    ## working directory, make sure it exists
    if wdir:
        wdir = os.path.abspath(wdir)
        if not os.path.exists(wdir):
            raise IPyradWarningExit(" working directory (wdir) does not exist")
    else:
        wdir = os.path.curdir

    ## output file path
    name = name.rsplit(".cf")[0]
    outfile = os.path.join(wdir, "{}.cf".format(name))
    out = open(outfile, 'w')

    ## parse loci file
    with open(locifile) as inloc:
        loci = inloc.read().strip().split("|\n")    

    ## get all names
    names = list(itertools.chain(*popdict.values()))
    popkeys = sorted(popdict.keys())

    ## count nsites
    nsites = sum(len(loc.split("\n")[0].split()[1]) for loc in loci[:])

    ## print the header 
    out.write(HEADER.format(**{"NPOP": len(popdict),
                               "NSITES": nsites,
                               "VTAXA": "\t".join(popkeys)}))
    
    ## build print string
    outstr = "chr{:<8}  {:<4}  "
    for cidx in xrange(len(popkeys)):
        outstr += "{:<8}  "
    
    toprint = []
    for idx in xrange(len(loci)):
        dat = loci[idx].split("\n")
        seqs = np.array([list(i.split()[1]) for i in dat[:-1]])
        names = [i.split()[0] for i in dat[:-1]]
        data = np.zeros((seqs.shape[1], len(popkeys), 4), dtype=np.uint16)

        for sidx in xrange(seqs.shape[1]):
            for cidx in xrange(len(popkeys)):               
                for name in popdict[popkeys[cidx]]:
                    if name in names:
                        base = seqs[names.index(name), sidx]
                        if base in list("ACGT"):
                            data[sidx, cidx, BASE2IDX[base]] += 2
                        elif base in list("RSYMKW"):
                            base1, base2 = AMBIGS[base]
                            data[sidx, cidx, BASE2IDX[base1]] += 1
                            data[sidx, cidx, BASE2IDX[base2]] += 1
                        
            ## print string for one locus
            sdat = [",".join([str(i) for i in i.tolist()]) for i in data[sidx]]
            #print outstr.format(idx+1, sidx+1, *sdat)
            toprint.append(outstr.format(idx+1, sidx+1, *sdat))

        ## if 10K loci, then print and clear
        if not idx % 10000:
            out.write("\n".join(toprint)+"\n")
            toprint = []

    ## close handle
    out.write("\n".join(toprint)+"\n")
    out.close()