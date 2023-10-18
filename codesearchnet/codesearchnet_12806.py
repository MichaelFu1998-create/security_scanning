def update(assembly, idict, count):
    """ updates dictionary with the next .5M reads from the super long string 
    phylip file. Makes for faster reading. """

    data = iter(open(os.path.join(assembly.dirs.outfiles,
                     assembly.name+".phy"), 'r'))

    ntax, nchar = data.next().strip().split()

    ## read in max N bp at a time                                                                            
    for line in data:
        tax, seq = line.strip().split()
        idict[tax] = idict[tax][100000:]
        idict[tax] += seq[count:count+100000]
    del line

    return idict