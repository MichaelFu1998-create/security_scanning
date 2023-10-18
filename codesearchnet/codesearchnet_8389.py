def create():
    """Create LNVM device"""

    if env():
        cij.err("cij.lnvm.create: Invalid LNVM ENV")
        return 1

    nvme = cij.env_to_dict("NVME", ["DEV_NAME"])
    lnvm = cij.env_to_dict(PREFIX, EXPORTED + REQUIRED)
    cij.emph("lnvm.create: LNVM_DEV_NAME: %s" % lnvm["DEV_NAME"])

    cmd = ["nvme lnvm create -d %s -n %s -t %s -b %s -e %s -f" % (
        nvme["DEV_NAME"], lnvm["DEV_NAME"], lnvm["DEV_TYPE"], lnvm["BGN"], lnvm["END"])]
    rcode, _, _ = cij.ssh.command(cmd, shell=True)
    if rcode:
        cij.err("cij.lnvm.create: FAILED")
        return 1

    return 0