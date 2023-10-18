def get_meta(offset, length, output):
    """Get chunk meta of NVMe device"""

    if env():
        cij.err("cij.nvme.meta: Invalid NVMe ENV.")
        return 1

    nvme = cij.env_to_dict(PREFIX, EXPORTED + REQUIRED)

    max_size = 0x40000
    with open(output, "wb") as fout:
        for off in range(offset, length, max_size):
            size = min(length - off, max_size)
            cmd = ["nvme get-log",
                   nvme["DEV_PATH"],
                   "-i 0xca",
                   "-o 0x%x" % off,
                   "-l 0x%x" % size,
                   "-b"]
            status, stdout, _ = cij.ssh.command(cmd, shell=True)
            if status:
                cij.err("cij.nvme.meta: Error get chunk meta")
                return 1

            fout.write(stdout)

    return 0