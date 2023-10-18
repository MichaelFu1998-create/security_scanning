def get_quart_iter(tups):
    """ returns an iterator to grab four lines at a time """

    if tups[0].endswith(".gz"):
        ofunc = gzip.open
    else:
        ofunc = open

    ## create iterators 
    ofile1 = ofunc(tups[0], 'r')
    fr1 = iter(ofile1) 
    quart1 = itertools.izip(fr1, fr1, fr1, fr1)
    if tups[1]:
        ofile2 = ofunc(tups[1], 'r')
        fr2 = iter(ofile2)  
        quart2 = itertools.izip(fr2, fr2, fr2, fr2)
        quarts = itertools.izip(quart1, quart2)
    else:
        ofile2 = 0
        quarts = itertools.izip(quart1, iter(int, 1))

    ## make a generator
    def feedme(quarts):
        for quart in quarts:
            yield quart
    genquarts = feedme(quarts)

    ## return generator and handles
    return genquarts, ofile1, ofile2