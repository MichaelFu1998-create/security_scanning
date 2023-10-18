def cat_file(path):
    """Cat file and return content"""

    cmd = ["cat", path]
    status, stdout, _ = cij.ssh.command(cmd, shell=True, echo=True)
    if status:
        raise RuntimeError("cij.nvme.env: cat %s failed" % path)
    return stdout.strip()