def condor_call(cmd, shell=True):
    """
    Tries to submit cmd to HTCondor, if it does not succeed, it will
    be called with subprocess.call.

    Parameters
    ----------
    cmd: string
        Command to be submitted

    Returns
    -------
    """
    log.info(cmd)
    ret = condor_submit(cmd)
    if ret != 0:
        subprocess.call(cmd, shell=shell)