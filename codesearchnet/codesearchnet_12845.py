def _zbufcountlines(filename, gzipped):
    """ faster line counter """
    if gzipped:
        cmd1 = ["gunzip", "-c", filename]
    else:
        cmd1 = ["cat", filename]
    cmd2 = ["wc"]

    proc1 = sps.Popen(cmd1, stdout=sps.PIPE, stderr=sps.PIPE)
    proc2 = sps.Popen(cmd2, stdin=proc1.stdout, stdout=sps.PIPE, stderr=sps.PIPE)
    res = proc2.communicate()[0]
    if proc2.returncode:
        raise IPyradWarningExit("error zbufcountlines {}:".format(res))
    LOGGER.info(res)
    nlines = int(res.split()[0])
    return nlines