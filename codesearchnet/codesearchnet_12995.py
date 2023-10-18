def ucount(sitecol):
    """
    Used to count the number of unique bases in a site for snpstring.
    returns as a spstring with * and -
    """

    ## a list for only catgs
    catg = [i for i in sitecol if i in "CATG"]

    ## find sites that are ambigs
    where = [sitecol[sitecol == i] for i in "RSKYWM"]

    ## for each occurrence of RSKWYM add ambig resolution to catg
    for ambig in where:
        for _ in range(ambig.size):
            catg += list(AMBIGS[ambig[0]])

    ## if invariant return " "
    if len(set(catg)) < 2:
        return " "
    else:
        ## get second most common site
        second = Counter(catg).most_common()[1][1]
        if second > 1:
            return "*"
        else:
            return "-"