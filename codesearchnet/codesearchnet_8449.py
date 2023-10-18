def env():
    """Verify NVME variables and construct exported variables"""

    if cij.ssh.env():
        cij.err("cij.nvm.env: invalid SSH environment")
        return 1

    nvm = cij.env_to_dict(PREFIX, REQUIRED)

    if "nvme" in nvm["DEV_NAME"]:
        nvm["DEV_PATH"] = "/dev/%s" % nvm["DEV_NAME"]
    else:
        nvm["DEV_PATH"] = "traddr:%s" % nvm["DEV_NAME"]

    cij.env_export(PREFIX, EXPORTED, nvm)

    return 0