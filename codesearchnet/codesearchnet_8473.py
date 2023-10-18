def pull(src, dst, folder=False):
    """SSH: pull data from remote linux"""

    if env():
        cij.err("cij.ssh.pull: Invalid SSH environment")
        return 1

    args = []

    if cij.ENV.get("SSH_KEY"):
        args.append("-i")
        args.append(cij.ENV.get("SSH_KEY"))

    if cij.ENV.get("SSH_PORT"):
        args.append("-P")
        args.append(cij.ENV.get("SSH_PORT"))

    if folder:
        args.append("-r")

    target = "%s:%s" % ("@".join([cij.ENV.get("SSH_USER"), cij.ENV.get("SSH_HOST")]), src)
    wrapped = ["scp", " ".join(args), target, dst]

    return cij.util.execute(wrapped, shell=True, echo=True)