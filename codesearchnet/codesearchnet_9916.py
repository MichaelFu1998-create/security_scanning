def update_running_pids(old_procs):
    """
        Update the list of the running process and return the list
    """
    new_procs = []
    for proc in old_procs:
        if proc.poll() is None and check_pid(proc.pid):
            publisher.debug(str(proc.pid) + ' is alive')
            new_procs.append(proc)
        else:
            try:
                publisher.debug(str(proc.pid) + ' is gone')
                os.kill(proc.pid, signal.SIGKILL)
            except:
                # the process is just already gone
                pass
    return new_procs