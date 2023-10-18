def get_all_checkpoints(rundir="runinfo"):
    """Finds the checkpoints from all last runs.

    Note that checkpoints are incremental, and this helper will not find
    previous checkpoints from earlier than the most recent run. It probably
    should be made to do so.

    Kwargs:
       - rundir(str) : Path to the runinfo directory

    Returns:
       - a list suitable for the checkpointFiles parameter of DataFlowKernel
         constructor

    """

    if(not os.path.isdir(rundir)):
        return []

    dirs = sorted(os.listdir(rundir))

    checkpoints = []

    for runid in dirs:

        checkpoint = os.path.abspath('{}/{}/checkpoint'.format(rundir, runid))

        if os.path.isdir(checkpoint):
            checkpoints.append(checkpoint)

    return checkpoints