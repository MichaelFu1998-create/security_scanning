def get_last_checkpoint(rundir="runinfo"):
    """Find the checkpoint from the last run, if one exists.

    Note that checkpoints are incremental, and this helper will not find
    previous checkpoints from earlier than the most recent run. It probably
    should be made to do so.

    Kwargs:
       - rundir(str) : Path to the runinfo directory

    Returns:
     - a list suitable for checkpointFiles parameter of DataFlowKernel
       constructor, with 0 or 1 elements

    """
    if not os.path.isdir(rundir):
        return []

    dirs = sorted(os.listdir(rundir))

    if len(dirs) == 0:
        return []

    last_runid = dirs[-1]
    last_checkpoint = os.path.abspath('{}/{}/checkpoint'.format(rundir, last_runid))

    if(not(os.path.isdir(last_checkpoint))):
        return []

    return [last_checkpoint]