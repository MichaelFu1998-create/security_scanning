def exists():
    """Verify that the ENV defined NVMe device exists"""

    if env():
        cij.err("cij.nvm.exists: Invalid NVMe ENV.")
        return 1

    nvm = cij.env_to_dict(PREFIX, EXPORTED + REQUIRED)

    cmd = ['[[ -b "%s" ]]' % nvm["DEV_PATH"]]
    rcode, _, _ = cij.ssh.command(cmd, shell=True, echo=False)

    return rcode