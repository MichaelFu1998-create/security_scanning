def tsuite_exit(trun, tsuite):
    """Triggers when exiting the given testsuite"""

    if trun["conf"]["VERBOSE"]:
        cij.emph("rnr:tsuite:exit")

    rcode = 0
    for hook in reversed(tsuite["hooks"]["exit"]):      # EXIT-hooks
        rcode = script_run(trun, hook)
        if rcode:
            break

    if trun["conf"]["VERBOSE"]:
        cij.emph("rnr:tsuite:exit { rcode: %r } " % rcode, rcode)

    return rcode