def check_synced(localval, comm=None):
    """
    It's common to forget to initialize your variables to the same values, or
    (less commonly) if you update them in some other way than adam, to get them out of sync.
    This function checks that variables on all MPI workers are the same, and raises
    an AssertionError otherwise

    Arguments:
        comm: MPI communicator
        localval: list of local variables (list of variables on current worker to be compared with the other workers)
    """
    comm = comm or MPI.COMM_WORLD
    vals = comm.gather(localval)
    if comm.rank == 0:
        assert all(val==vals[0] for val in vals[1:])