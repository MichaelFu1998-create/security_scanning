def command(cmd, shell=True, echo=True, suffix=None):
    """SSH: Run the given command over SSH as defined in environment"""

    if env():
        cij.err("cij.ssh.command: Invalid SSH environment")
        return 1

    prefix = []

    if cij.ENV.get("SSH_CMD_TIME") == "1":
        prefix.append("/usr/bin/time")

    if cij.ENV.get("SSH_CMD_TIMEOUT"):
        prefix.append("timeout")
        prefix.append(cij.ENV.get("SSH_CMD_TIMEOUT"))

    prefix.append("ssh")

    args = []

    if cij.ENV.get("SSH_KEY"):
        args.append("-i")
        args.append(cij.ENV.get("SSH_KEY"))

    if cij.ENV.get("SSH_PORT"):
        args.append("-p")
        args.append(cij.ENV.get("SSH_PORT"))

    args.append("@".join([cij.ENV.get("SSH_USER"), cij.ENV.get("SSH_HOST")]))

    wrapped = prefix + args + ["'%s'" % " ".join(cmd)]
    if suffix:
        wrapped += suffix

    return cij.util.execute(wrapped, shell, echo)