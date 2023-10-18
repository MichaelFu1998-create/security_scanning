def reboot(timeout=300, extra=""):
    """Reboot target"""

    if env():
        cij.err("cij.ssh.reboot: Invalid SSH environment")
        return 1

    timeout_backup = cij.ENV.get("SSH_CMD_TIMEOUT")

    try:
        time_start = time.time()
        status, last_uptime, _ = command(["/usr/bin/uptime -s"], shell=True, echo=False)
        if status:
            return 1

        cij.ENV["SSH_CMD_TIMEOUT"] = "3"
        cij.info("cij.ssh.reboot: Target: %s" % cij.ENV.get("SSH_HOST"))
        command(["reboot %s" % extra], shell=True, echo=False)

        while True:
            time_current = time.time()
            if (time_current - time_start) > timeout:
                cij.err("cij.ssh.reboot: Timeout")
                return 1

            status, current_uptime, _ = command(["/usr/bin/uptime -s"], shell=True, echo=False)
            if not status and current_uptime != last_uptime:
                break

        cij.info("cij.ssh.reboot: Time elapsed: %d seconds" % (time_current - time_start))

    finally:
        if timeout_backup is None:
            del cij.ENV["SSH_CMD_TIMEOUT"]
        else:
            cij.ENV["SSH_CMD_TIMEOUT"] = timeout_backup

    return 0