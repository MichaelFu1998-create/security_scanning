def pkill():
    """Kill all of FIO processes"""

    if env():
        return 1

    cmd = ["ps -aux | grep fio | grep -v grep"]
    status, _, _ = cij.ssh.command(cmd, shell=True, echo=False)
    if not status:
        status, _, _ = cij.ssh.command(["pkill -f fio"], shell=True)
        if status:
            return 1
    return 0