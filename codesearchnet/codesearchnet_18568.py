def check_pidfile(pidfile, debug):
    """Check that a process is not running more than once, using PIDFILE"""
    # Check PID exists and see if the PID is running
    if os.path.isfile(pidfile):
        pidfile_handle = open(pidfile, 'r')
        # try and read the PID file. If no luck, remove it
        try:
            pid = int(pidfile_handle.read())
            pidfile_handle.close()
            if check_pid(pid, debug):
                return True
        except:
            pass

        # PID is not active, remove the PID file
        os.unlink(pidfile)

    # Create a PID file, to ensure this is script is only run once (at a time)
    pid = str(os.getpid())
    open(pidfile, 'w').write(pid)
    return False