def write_ctl(name, imap, guidetree, nloci,
              infer_sptree, infer_delimit, delimit_alg,
              seed, burnin, nsample, sampfreq,
              thetaprior, tauprior, traits_df, nu0, kappa0,
              cleandata, useseqdata, usetraitdata, wdir,
              finetune, verbose):

    """ write outfile with any args in argdict """

    ## A string to store ctl info
    ctl = []

    ## check the tree (can do this better once we install ete3 w/ ipyrad)
    if not guidetree.endswith(";"):
        guidetree += ";"

    ## if traits_df then we make '.ibpp' files
    prog = 'bpp'
    if isinstance(traits_df, pd.DataFrame):
        prog = 'ibpp'

    ## write the top header info
    ctl.append("seed = {}".format(seed))
    ctl.append("seqfile = {}.{}.seq.txt".format(OPJ(wdir, name), prog))
    ctl.append("Imapfile = {}.{}.imap.txt".format(OPJ(wdir, name), prog))
    ctl.append("mcmcfile = {}.{}.mcmc.txt".format(OPJ(wdir, name), prog))
    ctl.append("outfile = {}.{}.out.txt".format(OPJ(wdir, name), prog))
    if isinstance(traits_df, pd.DataFrame):
        ctl.append("traitfile = {}.{}.traits.txt".format(OPJ(wdir, name), prog))

    ## number of loci (checks that seq file exists and parses from there)
    ctl.append("nloci = {}".format(nloci))
    ctl.append("usedata = {}".format(useseqdata))
    ctl.append("cleandata = {}".format(cleandata))

    ## infer species tree
    if infer_sptree:
        ctl.append("speciestree = 1 0.4 0.2 0.1")
    else:
        ctl.append("speciestree = 0")

    ## infer delimitation (with algorithm 1 by default)
    ctl.append("speciesdelimitation = {} {} {}"\
               .format(infer_delimit, delimit_alg[0],
                       " ".join([str(i) for i in delimit_alg[1:]])))

    ## if using iBPP (if not traits_df, we assume you're using bpp (v.3.3+)
    if isinstance(traits_df, pd.DataFrame):
        ## check that the data frame is properly formatted
        try:
            traits_df.values.astype(float)
        except Exception:
            raise IPyradWarningExit(PDREAD_ERROR)

        ## subsample to keep only samples that are in IMAP, we do not need to
        ## standarize traits b/c ibpp does that for us.
        samples = sorted(list(itertools.chain(*imap.values())))
        didx = [list(traits_df.index).index(i) for i in traits_df.index \
                if i not in samples]
        dtraits = traits_df.drop(traits_df.index[didx])

        ## mean standardize traits values after excluding samples
        straits = dtraits.apply(lambda x: (x - x.mean()) / (x.std()))

        ## convert NaN to "NA" cuz that's what ibpp likes, and write to file
        ftraits = straits.fillna("NA")
        traitdict = ftraits.T.to_dict("list")

        ## get reverse imap dict
        rev = {val:key for key in sorted(imap) for val in imap[key]}

        ## write trait file
        traitfile = "{}.{}.traits.txt".format(os.path.join(wdir, name), prog)
        with open(traitfile, 'w') as tout:
            tout.write("Indiv\n")
            tout.write("\t".join(
                ['Species'] + list(ftraits.columns))+"\n"
                )
            #for key in sorted(traitdict):
            #    tout.write("\t".join([key, rev[key]] + \
            #        ["^"+str(i) for i in traitdict[key]])+"\n"
            #        )
            nindT = 0
            for ikey in sorted(imap.keys()):
                samps = imap[ikey]
                for samp in sorted(samps):
                    if samp in traitdict:
                        tout.write("\t".join([samp, rev[samp]] + \
                            [str(i) for i in traitdict[samp]])+"\n"
                        )
                        nindT += 1

        #    tout.write("Indiv\n"+"\t".join(["Species"]+\
        #    ["t_{}".format(i) for i in range(len(traitdict.values()[0]))])+"\n")
        #    for key in sorted(traitdict):
        #        print >>tout, "\t".join([key, rev[key]] + \
        #                                [str(i) for i in traitdict[key]])
        #ftraits.to_csv(traitfile)

        ## write ntraits and nindT and traitfilename
        ctl.append("ntraits = {}".format(traits_df.shape[1]))
        ctl.append("nindT = {}".format(nindT))  #traits_df.shape[0]))
        ctl.append("usetraitdata = {}".format(usetraitdata))
        ctl.append("useseqdata = {}".format(useseqdata))

        ## trait priors
        ctl.append("nu0 = {}".format(nu0))
        ctl.append("kappa0 = {}".format(kappa0))

        ## remove ibpp incompatible options
        ctl.remove("usedata = {}".format(useseqdata))
        ctl.remove("speciestree = {}".format(infer_sptree))

    ## get tree values
    nspecies = str(len(imap))
    species = " ".join(sorted(imap))
    ninds = " ".join([str(len(imap[i])) for i in sorted(imap)])

    ## write the tree
    ctl.append("""\
species&tree = {} {}
                 {}
                 {}""".format(nspecies, species, ninds, guidetree))


    ## priors
    ctl.append("thetaprior = {} {}".format(*thetaprior))
    ctl.append("tauprior = {} {} {}".format(*tauprior))

    ## other values, fixed for now
    ctl.append("finetune = 1: {}".format(" ".join([str(i) for i in finetune])))
    #CTL.append("finetune = 1: 1 0.002 0.01 0.01 0.02 0.005 1.0")
    ctl.append("print = 1 0 0 0")
    ctl.append("burnin = {}".format(burnin))
    ctl.append("sampfreq = {}".format(sampfreq))
    ctl.append("nsample = {}".format(nsample))

    ## write out the ctl file
    with open("{}.{}.ctl.txt".format(OPJ(wdir, name), prog), 'w') as out:
        out.write("\n".join(ctl))

    ## if verbose print ctl
    if verbose:
        sys.stderr.write("ctl file\n--------\n"+"\n".join(ctl)+"\n--------\n\n")