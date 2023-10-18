def makephy(data, samples, longname):
    """ builds phy output. If large files writes 50000 loci at a time to tmp
    files and rebuilds at the end"""

    ## order names
    names = [i.name for i in samples]
    names.sort()
    
    ## read in loci file
    locifile = os.path.join(data.dirs.outfiles, data.name+".loci")
    locus = iter(open(locifile, 'rb'))

    ## dict for saving the full matrix
    fdict = {name:[] for name in names}

    ## list for saving locus number and locus range for partitions
    partitions = []
    initial_pos = 1

    ## remove empty column sites and append edited seqs to dict F
    done = 0
    nloci = 0
    nbases = 0

    ## TODO: This should be fixed. it cycles through reading each locus
    ## until nloci is less than this large number. It should really just
    ## read to the end of the file, so it'll do all loci no matter how
    ## many there are.
    while nloci < 5000000: 
        seqs = []
        #arrayed = np.array([])
        anames = []
        while 1:
            ## get next locus
            try:
                samp = locus.next()
            except StopIteration:
                done = 1
                break
            if "//" in samp:
                nloci += 1
                break
            else:
                try:
                    name, seq = samp.split()
                except ValueError:
                    print samp
                anames.append(name[1:])
                seqs.append(seq.strip())
        ## reset
        arrayed = np.array([list(i) for i in seqs])
        if done:
            break
        ## create mask for columns that are empty or 
        ## that are paired-end separators (compatible w/ pyrad v2 and v3)
        #mask = [i for i in range(len(arrayed.T)) if np.any([
        ## still surely a better way to vectorize this...
        mask = [i for i in arrayed.T if any([j not in list("-Nn") for j in i])]
        masked = np.dstack(mask)[0]

        ## partition information
        loc_name = "p"+str(nloci)
        loc_range = str(initial_pos) + "-" +\
                    str(len(masked[0]) + initial_pos -1)
        initial_pos += len(masked[0])
        partitions.append(loc_name+"="+loc_range)

        ## uncomment to print block info (used to partition by locus)
        #blockend += minray
        #print blockend,
        #print loc
        #print arrayed

        ## append data to dict
        for name in names:
            if name in anames:
                #fdict[name].append(arrayed[anames.index(name), mask].tostring())
                fdict[name].append(masked[anames.index(name),:].tostring())
            else:
                fdict[name].append("N"*masked.shape[1])
                #fdict[name].append("N"*len(arrayed[0, mask]))
        ## add len to total length
        nbases += len(fdict[name][-1])

        ## after x iterations tmp pickle fdict?
        if not nloci % 1e4:
            ## concat strings
            for name in fdict:
                with open(os.path.join(assembly.dirs.outfiles , "tmp", 
                    "{}_{}.phy.tmp".format(name, nloci)), 'wb') as wout:
                    wout.write("".join(fdict[name]))
            del fdict
            fdict = {name:[] for name in names}

    ## print out .PHY file, if really big, pull form multiple tmp pickle
    superout = open(os.path.join( assembly.dirs.outfiles, assembly.name+".phy" ), 'wb')
    print >>superout, len(names), nbases
    if nloci < 1e4:
        for name in names:
            print >>superout, name+(" "*((longname+3)-\
                              len(name)))+"".join(fdict[name])
    else:
        for name in names:
            superout.write("{}{}{}".format(
                            name,
                            " "*((longname+3)-len(name)),
                            "".join(fdict[name])))
            tmpfiles = glob.glob(os.path.join(assembly.dirs.outfiles, "tmp", name+"*.phy.tmp"))
            tmpfiles.sort()
            for tmpf in tmpfiles:
                with open(tmpf, 'rb') as tmpin:
                    superout.write(tmpin.read())
                os.remove(tmpf)
            superout.write("\n")
    superout.close()
    raxml_part_out = open(os.path.join(assembly.dirs.outfiles, assembly.name+".phy.partitions"), 'w')
    for partition in partitions:
        print >>raxml_part_out, "DNA, %s" % (partition)
    raxml_part_out.close()

    return partitions