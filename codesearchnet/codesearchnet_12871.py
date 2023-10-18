def find3radbcode(cutters, longbar, read1):
    """ find barcode sequence in the beginning of read """
    ## default barcode string
    for ambigcuts in cutters:
        for cutter in ambigcuts:
            ## If the cutter is unambiguous there will only be one.
            if not cutter:
                continue
            search = read1[1][:int(longbar[0]+len(cutter)+1)]
            splitsearch = search.rsplit(cutter, 1)
            if len(splitsearch) > 1:
                return splitsearch[0]
    ## No cutter found
    return splitsearch[0]