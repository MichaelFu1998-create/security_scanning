def _combineResults(result, *namedTuples):
    """ Return a list of namedtuples from the result of a join query.  A
    single database result is partitioned at intervals corresponding to the
    fields in namedTuples.  The return value is the result of applying
    namedtuple._make() to each of the partitions, for each of the namedTuples.

    Parameters:
    ----------------------------------------------------------------
    result:         Tuple representing a single result from a database query
    *namedTuples:   List of named tuples.

    """
    results = ClientJobsDAO.partitionAtIntervals(
      result, [len(nt._fields) for nt in namedTuples])
    return [nt._make(result) for nt, result in zip(namedTuples, results)]