def argsort(data, out=None, chunksize=None, 
        baseargsort=None, 
        argmerge=None, np=None):
    """
     parallel argsort, like numpy.argsort

     use sizeof(intp) * len(data) as scratch space

     use baseargsort for serial sort 
         ind = baseargsort(data)

     use argmerge to merge
         def argmerge(data, A, B, out):
             ensure data[out] is sorted
             and out[:] = A join B

     TODO: shall try to use the inplace merge mentioned in 
            http://keithschwarz.com/interesting/code/?dir=inplace-merge.
    """
    if baseargsort is None:
        baseargsort = lambda x:x.argsort()

    if argmerge is None:
        argmerge = default_argmerge

    if chunksize is None:
        chunksize = 1024 * 1024 * 16

    if out is None:
        arg1 = numpy.empty(len(data), dtype='intp')
        out = arg1
    else:
        assert out.dtype == numpy.dtype('intp')
        assert len(out) == len(data)
        arg1 = out

    if np is None:
        np = sharedmem.cpu_count()

    if np <= 1 or len(data) < chunksize: 
        out[:] = baseargsort(data)
        return out

    CHK = [slice(i, i + chunksize) for i in range(0, len(data), chunksize)]
    DUMMY = slice(len(data), len(data))
    if len(CHK) % 2: CHK.append(DUMMY)
    with sharedmem.TPool() as pool:
        def work(i):
            C = CHK[i]
            start, stop, step = C.indices(len(data))
            arg1[C] = baseargsort(data[C])
            arg1[C] += start
        pool.map(work, range(len(CHK)))
  
    arg2 = numpy.empty_like(arg1)
  
    flip = 0
    while len(CHK) > 1:
        with sharedmem.TPool() as pool:
            def work(i):
                C1 = CHK[i]
                C2 = CHK[i+1]
                start1, stop1, step1 = C1.indices(len(data))
                start2, stop2, step2 = C2.indices(len(data))
        #        print 'argmerge', start1, stop1, start2, stop2
                assert start2 == stop1
                argmerge(data, arg1[C1], arg1[C2], arg2[start1:stop2])
                return slice(start1, stop2)
            CHK = pool.map(work, range(0, len(CHK), 2))
            arg1, arg2 = arg2, arg1
            flip = flip + 1
        if len(CHK) == 1: break
        if len(CHK) % 2: CHK.append(DUMMY)
    if flip % 2 != 0:
        # only even flips out ends up pointing to arg2 and needs to be
        # copied
        out[:] = arg1
    return out