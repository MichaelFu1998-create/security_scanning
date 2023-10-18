def condor_submit(cmd):
    """
    Submits cmd to HTCondor queue

    Parameters
    ----------
    cmd: string
        Command to be submitted

    Returns
    -------
    int
        returncode value from calling the submission command.
    """
    is_running = subprocess.call('condor_status', shell=True) == 0
    if not is_running:
        raise CalledProcessError('HTCondor is not running.')

    sub_cmd = 'condor_qsub -shell n -b y -r y -N ' \
              + cmd.split()[0] + ' -m n'

    log.info('Calling: ' + sub_cmd)

    return subprocess.call(sub_cmd + ' ' + cmd, shell=True)