def makenex(assembly, names, longname, partitions):
    """ PRINT NEXUS """

    ## make nexus output
    data = iter(open(os.path.join(assembly.dirs.outfiles, assembly.name+".phy" ), 'r' ))
    nexout = open(os.path.join(assembly.dirs.outfiles, assembly.name+".nex" ), 'wb' )

    ntax, nchar = data.next().strip().split(" ")

    print >>nexout, "#NEXUS"
    print >>nexout, "BEGIN DATA;"
    print >>nexout, "  DIMENSIONS NTAX=%s NCHAR=%s;" % (ntax,nchar)
    print >>nexout, "  FORMAT DATATYPE=DNA MISSING=N GAP=- INTERLEAVE=YES;"
    print >>nexout, "  MATRIX"

    idict = {}

    ## read in max 1M bp at a time
    for line in data:
        tax, seq = line.strip().split()
        idict[tax] = seq[0:100000]
    del line

    nameorder = idict.keys()
    nameorder.sort()

    n=0
    tempn=0
    sz = 100
    while n < len(seq):
        for tax in nameorder:
            print >>nexout, "  "+tax+" "*\
                             ((longname-len(tax))+3)+\
                             idict[tax][tempn:tempn+sz]
        n += sz
        tempn += sz
        print >>nexout, ""

        if not n % 100000:
            #print idict[tax][tempn:tempn+sz]
            idict = update(assembly, idict, n)
            tempn -= 100000
            
    print >>nexout, ';'
    print >>nexout, 'END;'
    
    ### partitions info
    print >>nexout, "BEGIN SETS;"
    for partition in partitions:
        print >>nexout, "  CHARSET %s;" % (partition)
    print >>nexout, "END;"

    nexout.close()