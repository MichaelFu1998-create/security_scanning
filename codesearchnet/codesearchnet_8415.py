def tsuite_enter(trun, tsuite):
    """Triggers when entering the given testsuite"""

    if trun["conf"]["VERBOSE"]:
        cij.emph("rnr:tsuite:enter { name: %r }" % tsuite["name"])

    rcode = 0
    for hook in tsuite["hooks"]["enter"]:     # ENTER-hooks
        rcode = script_run(trun, hook)
        if rcode:
            break

    if trun["conf"]["VERBOSE"]:
        cij.emph("rnr:tsuite:enter { rcode: %r } " % rcode, rcode)

    return rcode