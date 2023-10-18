def setup_mpi_gpus():
    """
    Set CUDA_VISIBLE_DEVICES to MPI rank if not already set
    """
    if 'CUDA_VISIBLE_DEVICES' not in os.environ:
        if sys.platform == 'darwin': # This Assumes if you're on OSX you're just
            ids = []                 # doing a smoke test and don't want GPUs
        else:
            lrank, _lsize = get_local_rank_size(MPI.COMM_WORLD)
            ids = [lrank]
        os.environ["CUDA_VISIBLE_DEVICES"] = ",".join(map(str, ids))