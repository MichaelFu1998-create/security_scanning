def worker(self):
    """ 
    Calculates the quartet weights for the test at a random
    subsampled chunk of loci.
    """

    ## subsample loci 
    fullseqs = self.sample_loci()

    ## find all iterations of samples for this quartet
    liters = itertools.product(*self.imap.values())

    ## run tree inference for each iteration of sampledict
    hashval = uuid.uuid4().hex
    weights = []
    for ridx, lidx in enumerate(liters):
        
        ## get subalignment for this iteration and make to nex
        a,b,c,d = lidx
        sub = {}
        for i in lidx:
            if self.rmap[i] == "p1":
                sub["A"] = fullseqs[i]
            elif self.rmap[i] == "p2":
                sub["B"] = fullseqs[i]
            elif self.rmap[i] == "p3":
                sub["C"] = fullseqs[i]
            else:
                sub["D"] = fullseqs[i]
                
        ## write as nexus file
        nex = []
        for tax in list("ABCD"):
            nex.append(">{}         {}".format(tax, sub[tax]))
            
        ## check for too much missing or lack of variants
        nsites, nvar = count_var(nex)

        ## only run test if there's variation present
        if nvar > self.minsnps:
               
            ## format as nexus file
            nexus = "{} {}\n".format(4, len(fullseqs[a])) + "\n".join(nex)    

            ## infer ML tree
            treeorder = self.run_tree_inference(nexus, "{}.{}".format(hashval, ridx))

            ## add to list
            weights.append(treeorder)

    ## cleanup - remove all files with the hash val
    rfiles = glob.glob(os.path.join(tempfile.tempdir, "*{}*".format(hashval)))
    for rfile in rfiles:
        if os.path.exists(rfile):
            os.remove(rfile)

    ## return result as weights for the set topologies.
    trees = ["ABCD", "ACBD", "ADBC"]
    wdict = {i:float(weights.count(i))/len(weights) for i in trees}
    return wdict