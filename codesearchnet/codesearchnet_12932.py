def sort_seeds(uhandle, usort):
    """ sort seeds from cluster results"""
    cmd = ["sort", "-k", "2", uhandle, "-o", usort]
    proc = sps.Popen(cmd, close_fds=True)
    proc.communicate()