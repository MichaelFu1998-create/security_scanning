def grompp_qtot(*args, **kwargs):
    """Run ``gromacs.grompp`` and return the total charge of the  system.

    :Arguments:
       The arguments are the ones one would pass to :func:`gromacs.grompp`.
    :Returns:
       The total charge as reported

    Some things to keep in mind:

    * The stdout output of grompp is only shown when an error occurs. For
      debugging, look at the log file or screen output and try running the
      normal :func:`gromacs.grompp` command and analyze the output if the
      debugging messages are not sufficient.

    * Check that ``qtot`` is correct. Because the function is based on pattern
      matching of the informative output of :program:`grompp` it can break when
      the output format changes. This version recognizes lines like ::

            '  System has non-zero total charge: -4.000001e+00'

      using the regular expression
      :regexp:`System has non-zero total charge: *(?P<qtot>[-+]?\d*\.\d+([eE][-+]\d+)?)`.

    """
    qtot_pattern = re.compile('System has non-zero total charge: *(?P<qtot>[-+]?\d*\.\d+([eE][-+]\d+)?)')
    # make sure to capture ALL output
    kwargs['stdout'] = False
    kwargs['stderr'] = False
    rc, output, error = grompp_warnonly(*args, **kwargs)
    gmxoutput = "\n".join([x for x in [output, error] if x is not None])
    if rc != 0:
        # error occured and we want to see the whole output for debugging
        msg = "grompp_qtot() failed. See warning and screen output for clues."
        logger.error(msg)
        import sys
        sys.stderr.write("=========== grompp (stdout/stderr) ============\n")
        sys.stderr.write(gmxoutput)
        sys.stderr.write("===============================================\n")
        sys.stderr.flush()
        raise GromacsError(rc, msg)
    qtot = 0
    for line in gmxoutput.split('\n'):
        m = qtot_pattern.search(line)
        if m:
            qtot = float(m.group('qtot'))
            break
    logger.info("system total charge qtot = {qtot!r}".format(**vars()))
    return qtot