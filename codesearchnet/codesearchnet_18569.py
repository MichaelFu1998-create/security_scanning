def check_pid(pid, debug):
    """This function will check whether a PID is currently running"""
    try:
        # A Kill of 0 is to check if the PID is active. It won't kill the process
        os.kill(pid, 0)
        if debug > 1:
            print("Script has a PIDFILE where the process is still running")
        return True
    except OSError:
        if debug > 1:
            print("Script does not appear to be running")
        return False