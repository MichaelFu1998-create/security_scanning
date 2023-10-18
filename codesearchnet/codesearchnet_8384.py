def fmt(lbaf=3):
    """Do format for NVMe device"""

    if env():
        cij.err("cij.nvme.exists: Invalid NVMe ENV.")
        return 1

    nvme = cij.env_to_dict(PREFIX, EXPORTED + REQUIRED)

    cmd = ["nvme", "format", nvme["DEV_PATH"], "-l", str(lbaf)]
    rcode, _, _ = cij.ssh.command(cmd, shell=True)

    return rcode