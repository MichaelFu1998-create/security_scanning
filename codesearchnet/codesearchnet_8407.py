def env():
    """Verify BLOCK variables and construct exported variables"""

    if cij.ssh.env():
        cij.err("cij.block.env: invalid SSH environment")
        return 1

    block = cij.env_to_dict(PREFIX, REQUIRED)

    block["DEV_PATH"] = "/dev/%s" % block["DEV_NAME"]

    cij.env_export(PREFIX, EXPORTED, block)

    return 0