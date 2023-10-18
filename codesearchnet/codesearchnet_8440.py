def env():
    """Verify PCI variables and construct exported variables"""

    if cij.ssh.env():
        cij.err("cij.pci.env: invalid SSH environment")
        return 1

    pci = cij.env_to_dict(PREFIX, REQUIRED)

    pci["BUS_PATH"] = "/sys/bus/pci"
    pci["DEV_PATH"] = os.sep.join([pci["BUS_PATH"], "devices", pci["DEV_NAME"]])

    cij.env_export(PREFIX, EXPORTED, pci)

    return 0