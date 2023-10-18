def obtain_content_ranges(rangetext, filesize):
    """
   returns tuple (list, value)

   list
       content ranges as values to their parsed components in the tuple
       (seek_position/abs position of first byte, abs position of last byte, num_of_bytes_to_read)
   value
       total length for Content-Length
   """
    listReturn = []
    seqRanges = rangetext.split(",")
    for subrange in seqRanges:
        matched = False
        if not matched:
            mObj = reByteRangeSpecifier.search(subrange)
            if mObj:
                firstpos = int(mObj.group(2))
                if mObj.group(3) == "":
                    lastpos = filesize - 1
                else:
                    lastpos = int(mObj.group(3))
                if firstpos <= lastpos and firstpos < filesize:
                    if lastpos >= filesize:
                        lastpos = filesize - 1
                    listReturn.append((firstpos, lastpos))
                    matched = True
        if not matched:
            mObj = reSuffixByteRangeSpecifier.search(subrange)
            if mObj:
                firstpos = filesize - int(mObj.group(2))
                if firstpos < 0:
                    firstpos = 0
                lastpos = filesize - 1
                listReturn.append((firstpos, lastpos))

                matched = True

    # consolidate ranges
    listReturn.sort()
    listReturn2 = []
    totallength = 0
    while len(listReturn) > 0:
        (rfirstpos, rlastpos) = listReturn.pop()
        counter = len(listReturn)
        while counter > 0:
            (nfirstpos, nlastpos) = listReturn[counter - 1]
            if nlastpos < rfirstpos - 1 or nfirstpos > nlastpos + 1:
                pass
            else:
                rfirstpos = min(rfirstpos, nfirstpos)
                rlastpos = max(rlastpos, nlastpos)
                del listReturn[counter - 1]
            counter = counter - 1
        listReturn2.append((rfirstpos, rlastpos, rlastpos - rfirstpos + 1))
        totallength = totallength + rlastpos - rfirstpos + 1

    return (listReturn2, totallength)