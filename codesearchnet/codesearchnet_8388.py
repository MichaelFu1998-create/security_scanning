def env():
    """Verify LNVM variables and construct exported variables"""

    if cij.ssh.env():
        cij.err("cij.lnvm.env: invalid SSH environment")
        return 1

    lnvm = cij.env_to_dict(PREFIX, REQUIRED)
    nvme = cij.env_to_dict("NVME", ["DEV_NAME"])

    if "BGN" not in lnvm.keys():
        cij.err("cij.lnvm.env: invalid LNVM_BGN")
        return 1
    if "END" not in lnvm.keys():
        cij.err("cij.lnvm.env: invalid LNVM_END")
        return 1
    if "DEV_TYPE" not in lnvm.keys():
        cij.err("cij.lnvm.env: invalid LNVM_DEV_TYPE")
        return 1

    lnvm["DEV_NAME"] = "%sb%03de%03d" % (nvme["DEV_NAME"], int(lnvm["BGN"]), int(lnvm["END"]))
    lnvm["DEV_PATH"] = "/dev/%s" % lnvm["DEV_NAME"]

    cij.env_export(PREFIX, EXPORTED, lnvm)

    return 0