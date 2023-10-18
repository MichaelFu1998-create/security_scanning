def system(command, input=None):
    """commands.getoutput() replacement that also works on windows.

    Code mostly copied from zc.buildout.

    """
    logger.debug("Executing command: %s", command)
    p = subprocess.Popen(command,
                         shell=True,
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE,
                         close_fds=MUST_CLOSE_FDS)
    stdoutdata, stderrdata = p.communicate(input=input)
    result = stdoutdata + stderrdata
    if p.returncode:
        logger.error("Something went wrong when executing '%s'",
                     command)
        logger.error("Returncode: %s", p.returncode)
        logger.error("Output:")
        logger.error(result)
        sys.exit(1)
    logger.info(result)