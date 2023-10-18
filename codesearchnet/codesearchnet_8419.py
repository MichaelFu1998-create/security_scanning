def trun_exit(trun):
    """Triggers when exiting the given testrun"""

    if trun["conf"]["VERBOSE"]:
        cij.emph("rnr:trun:exit")

    rcode = 0
    for hook in reversed(trun["hooks"]["exit"]):    # EXIT-hooks
        rcode = script_run(trun, hook)
        if rcode:
            break

    if trun["conf"]["VERBOSE"]:
        cij.emph("rnr:trun::exit { rcode: %r }" % rcode, rcode)

    return rcode