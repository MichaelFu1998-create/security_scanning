def wait(timeout=300):
    """Wait util target connected"""

    if env():
        cij.err("cij.ssh.wait: Invalid SSH environment")
        return 1

    timeout_backup = cij.ENV.get("SSH_CMD_TIMEOUT")

    try:
        time_start = time.time()

        cij.ENV["SSH_CMD_TIMEOUT"] = "3"

        while True:
            time_current = time.time()
            if (time_current - time_start) > timeout:
                cij.err("cij.ssh.wait: Timeout")
                return 1

            status, _, _ = command(["exit"], shell=True, echo=False)
            if not status:
                break

        cij.info("cij.ssh.wait: Time elapsed: %d seconds" % (time_current - time_start))

    finally:
        if timeout_backup is None:
            del cij.ENV["SSH_CMD_TIMEOUT"]
        else:
            cij.ENV["SSH_CMD_TIMEOUT"] = timeout_backup

    return 0