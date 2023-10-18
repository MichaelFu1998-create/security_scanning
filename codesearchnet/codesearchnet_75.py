def dict_gather(comm, d, op='mean', assert_all_have_data=True):
    """
    Perform a reduction operation over dicts
    """
    if comm is None: return d
    alldicts = comm.allgather(d)
    size = comm.size
    k2li = defaultdict(list)
    for d in alldicts:
        for (k,v) in d.items():
            k2li[k].append(v)
    result = {}
    for (k,li) in k2li.items():
        if assert_all_have_data:
            assert len(li)==size, "only %i out of %i MPI workers have sent '%s'" % (len(li), size, k)
        if op=='mean':
            result[k] = np.mean(li, axis=0)
        elif op=='sum':
            result[k] = np.sum(li, axis=0)
        else:
            assert 0, op
    return result